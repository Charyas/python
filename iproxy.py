#coding=utf-8
import re
import requests
import time

import socket
from sgmllib import SGMLParser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import *

urls = ["http://www.xicidaili.com/nn",
	   ]


#'http://www.haodailiip.com/guonei'
#
#parse xici free proxy
class ListName(SGMLParser):
	def __init__(self):
		SGMLParser.__init__(self)
		self.ip = ""
		self.name = []

	def handle_data(self, text):
		if self.valid_ip(text):
			#print text
			self.ip = text
		if self.valid_port(text) and len(self.ip) != 0:
			self.ip = self.ip+":"+text
			self.name.append(self.ip)
			self.ip = ""

	def valid_ip(self, text):
		   pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
		   if re.match(pattern, text):
		      return True
		   else:
		      return False
	def valid_port(self, text):
		try:
			int(text)
			return True
		except:
			return False

def getPorxyIp(url):
	user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
	headers = {
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate, sdch',
		'Accept-Language':'en-US,en;q=0.8,zh;q=0.6',
		'Connection':'keep-alive',
		'Host':'www.xicidaili.com',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':user_agent
		}

	for i in range(1,2):
		url = url + "/"+ str(i)
		print url
		r = requests.get(url, headers=headers)
		listname = ListName()
		listname.feed(r.text)
		for item in listname.name:
			print item
			if item != None:
				writeFile(fp, item)

def writeFile(fp, content):
	fp.write(content + "\n")

def readFile(fp):
	buf = []
	buf = fp.readlines(10000000)
	return buf

def testproxy():
	service_args = ["--proxy=186.151.254.242:8080", '--proxy-type=http',]

	user_agent =('Mozilla/5.0 (Windows NT 6.1; WOW64) '+
		'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')
	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap['phantomjs.page.settings.userAgent'] = user_agent

	browser = webdriver.PhantomJS(executable_path="phantomjs.exe", desired_capabilities=dcap, service_args=service_args)
	browser.get("https://www.baidu.com/")
	browser.get_screenshot_as_file('1111.png')
	time.sleep(3)
	try:
		browser.get_screenshot_as_file('aaa.png')
		inputb = browser.find_element_by_id("kw")

		inputb.send_keys("ip")
		browser.get_screenshot_as_file('bbb.png')
		baidu = browser.find_element_by_id("su")
		baidu.submit()
		time.sleep(2)
		browser.get_screenshot_as_file('cccc.png')
	except:
		print "can't find error"

	browser.close()

global fp
if __name__ == '__main__':
	# fp = open("ppp.txt", "w+")
	# print getPorxyIp(urls[0])
	# fp.close()
	testproxy()
