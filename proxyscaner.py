#coding='utf-8'

import socket
import urllib2
import gzip
import requests
import re
# get user free ip from
#
#
#
#
def checkPort(host, port):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(3)
		s.content((host,port))
		s.close()
		return True
	except:
		return False

def checkProxy(host, port):
	proxy = "http://%s:%s"%(host, port)
	handle = urllib2.ProxyHandler({'http':proxy})
	opener = urllib2.build_opener(handle,urllib2.HTTPHandler)
	try:
		r = opener.open("http://www.baidu.com/img/baidu_jgylogo3.gif", timeout=5)
		l = len(r.read())
		print l
		if (l == 705):
			return True
		return False
	except Exception,e:
		return False

def valid_ip(self, text):
	   pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
	   if re.match(pattern, text):
	      return True
	   else:
	      return False

def checkip(proxy):
	handle = urllib2.ProxyHandler({'http':proxy})
	opener = urllib2.build_opener(handle,urllib2.HTTPHandler)
	try:
		r = opener.open("http://www.baidu.com/img/baidu_jgylogo3.gif", timeout=5)
		l = len(r.read())
		print l
		if (l == 705):
			return True
		return False
	except Exception,e:
		return False

def getyoudaili():
	url = 'http://www.youdaili.net/Daili/guonei'
	r = requests.get(url)
	print r.content
	# get all ip data page
	return
	pos1 = r.content.find('<p><span style="font-size:14px;">')
	pos2 = r.content.find('<div class="dede_pages">')
	print pos1,pos2

	content = r.content[pos1+len('<p><span style="font-size:14px;">'):pos2-5].split('\n')
	for line in content:
		pos = line.find('@')
		if pos < 0:
			continue
		line = line[:pos]
		if checkip(line):
			fp.write(line + '\n')

if __name__ == '__main__':
	global fp
	fp = open("aaa.txt", "w+")
	getyoudaili()

	fp.close()