#coding='utf-8'
import os
import sys
import socket
import urllib2
import datetime
import Queue
import threading
import platform

ports = [80, 8080]

def checkping(ip):
	platname = platform.platform()
	if platname.find('Windows') > 0:
		cmd = "ping -n 1 -w 1 %s"%ip
		info = os.popen(cmd).readlines()
		for line in info:
			pos = line.rfind("=")
			if pos < 0:
				continue
			xx = line[pos+1:pos+4]
			try:
				per = int(xx)
			except:
				return True
			return False
	else:
		cmd = "ping -c 1 -w 1 %s"%ip
		info = os.popen(cmd).readlines()
		for line in info:
			pos = line.find("loss")
			if pos < 0:
				continue
			xx = line[pos-12:pos-9]
			try:
				per = int(xx)
			except:
				return True
			return False

	return True

#49.64.0.0	49.95.255.255
def productip(start, end):
	startip = start.split('.')
	endip = end.split('.')

	ips = []

	for ip1 in range(int(startip[0]), int(endip[0]) + 1):
		for ip2 in range(int(startip[1]), int(endip[1]) + 1):
			for ip3 in range(int(startip[2]), int(endip[2]) + 1):
				for ip4 in range(int(startip[3]), int(endip[3]) + 1):
					ip = str(ip1)+'.'+str(ip2)+'.'+str(ip3)+'.'+str(ip4)
					if checkping(ip) == True:
						print "ping %s ok"%ip
						ips.append(ip)

	return ips

def checkip(proxy):
	handle = urllib2.ProxyHandler({'http':proxy})
	opener = urllib2.build_opener(handle,urllib2.HTTPHandler)
	try:
		r = opener.open("http://www.baidu.com/img/baidu_jgylogo3.gif", timeout=3)
		l = len(r.read())
		print l
		if (l == 705):
			return True
		return False
	except Exception,e:
		return False

def scanproxy(start, end):
	ips = productip(start, end)
	filename = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+'.txt'
	f = open(filename, "a+")
	for ip in ips:
		for i in range(0,2):
			proxy = ip+':'+str(ports[i])
			if checkip(proxy) == True:
				print "proxy:%s"%proxy
				f.writelines(proxy+'\n')
				f.flush()
	f.close()

class Task(threading.Thread):
	def __init__(self, queue, name=""):
		threading.Thread.__init__(self)
		self.kill = False
		self.queue = queue
		self.name = name
		self._isRunning = False
		self._waitToKill = False
	def run(self):
		while not self.kill:
			self._isRunning = False
			try:
				callback, args = self.queue.get(timeout=0.1)
				self._isRunning = True
				try:
					callback(*args)
				except:
					print >> sys.stderr,"callback Error: [%s] :" % self.name, e
			except:
				pass
			if self._waitToKill and not self._isRunning:
				self.kill = True
	def stop(self):
		self.kill = True
	def waitAndStop(self):
		self._waitToKill = True
	def isKilled(self):
		return self.kill

class Pool(object):
	def __init__(self, pool_size):
		self.pool_size = pool_size
		self.thread_list = []
		self.queue = Queue.Queue(pool_size)
		self._initThread()
	def _initThread(self):
		for i in range(0, self.pool_size):
			thr = Task(self.queue, "Thread " + str(i))
			self.thread_list.append(thr)
		for thr in self.thread_list:
			thr.start()
	def _removeDeadThreads(self):
		for thr in self.thread_list:
			if thr.isKilled():
				self.thread_list.remove(thr)
				del thr
	def delThreads(self, num):
		try:
			if self.thread_list == []:
				return
			for thr in self.thread_list:
				if num > 0:
					thr.stop()
					num -= 1
			self._removeDeadThreads()
		finally:
			pass
	def addThreads(self, num):
		try:
			self._removeDeadThreads()
			for cpt in range(num):
				thr=Task(self.queue, "new Thread " + str(cpt))
				thr.start()
				self.thread_list.append(thr)
		except:
			pass
	def stopAll(self):
		for thr in self.thread_list:
			thr.stop()
	def waitAndStopAll(self):
		for thr in self.thread_list:
			thr.waitAndStop()
	def joinAll(self):
		for thr in self.thread_list:
			thr.join()
	def countThreads(self):
		try:
			return len(self.thread_list)
		finally:
			pass
	def addTask(self, callback, args):
		try:
			self._removeDeadThreads()
			if self.thread_list == []:
				return
			self.queue.put((callback, args))
		finally:
			pass

if __name__ == '__main__':
	# need split smaller
	start = '49.64.0.0'
	#end = '49.95.255.255'
	end = '49.64.10.255'

	scanproxy(start, end)
