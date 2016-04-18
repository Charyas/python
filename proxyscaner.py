#coding='utf-8'

import socket
import urllib2
import gzip
import requests
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
from StringIO import StringIO
def getyoudaili():
	url = 'http://www.youdaili.net/Daili/guonei/4343.html'
	r = requests.get(url)
	pos1 = r.content.find('<p><span style="font-size:14px;">')
	pos2 = r.content.find('<div class="dede_pages">')
	print pos1,pos2

	new = r.content[pos1:pos2]
	print new

if __name__ == '__main__':
	getyoudaili()