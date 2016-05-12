#coding=utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys
import time
import random
import datetime
import urllib2

reload(sys)
sys.setdefaultencoding('utf-8')

def readagent(filename):
	userAngels = []
	f = open(filename, 'r')
	buf = f.readlines(1000000)
	f.close
	for line in buf:
		line = line.strip('\n')
		userAngels.append(line)

	return userAngels

def readscript(filename):
	scripts = []
	f = open(filename, 'r')
	buf = f.readlines(1000000)
	f.close
	for line in buf:
		line = line.strip('\n')
		scripts.append(line)
	return scripts

def readiproxy(filename):
	iproxy = []
	f = open(filename, 'r')
	buf = f.readlines(1000000)
	f.close
	for line in buf:
		line = line.strip('\n')
		iproxy.append(line)

	return iproxy

def checkip(proxy):
	handle = urllib2.ProxyHandler({'http':proxy})
	opener = urllib2.build_opener(handle,urllib2.HTTPHandler)
	try:
		r = opener.open("http://www.baidu.com/img/baidu_jgylogo3.gif", timeout=5)
		l = len(r.read())
		if (l == 705):
			return True
		return False
	except Exception,e:
		return False

#点击进入下一页
def nextpage(browser):
	nextpage = browser.find_element_by_id("page")
	pages = nextpage.find_elements_by_tag_name('a')
	#最后一个元素显示为下一页
	pages[len(pages) -1].click()

def newopen(browser, url):
	browser.get(url)
	WebDriverWait(browser, 5)

def searchKey(browser, key):
	inputb = browser.find_element_by_id("kw")
	inputb.send_keys(key.decode('utf-8'))

	baidu = browser.find_element_by_id("su")
	baidu.submit()

def login(url):
	# scripts = readscript("script")
	# script = random.sample(scripts, 1)[0]
	# userAngels = readagent("user_agent")
	# user_agent = str(random.sample(userAngels, 1)[0])
	#user_agent =('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')
	user_agent =('Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0')
	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap['phantomjs.page.settings.userAgent'] = user_agent
	# dcap['phantomjs.page.settings.loadImages'] = False
	# dcap['phantomjs.page.settings.resourceTimeout'] = 5*1000

	# iproxys = readiproxy("proxyip.txt")
	# iproxy=""
	# while (1):
	# 	iproxy = str(random.sample(iproxys, 1)[0])
	# 	#print iproxy
	# 	if checkip(iproxy):
	# 		break

	# service_args = ["--proxy=%s"%iproxy, '--proxy-type=http','--ignore-ssl-errors=true',]
	#service_args = ["--proxy=58.67.159.50:80", '--proxy-type=http',]
	#print service_args
	#browser = webdriver.PhantomJS(executable_path="phantomjs.exe", desired_capabilities=dcap, service_args=service_args)
	browser = webdriver.PhantomJS(executable_path="phantomjs.exe", desired_capabilities=dcap)
	# try:
	browser.get(str(url))
	WebDriverWait(browser, 5)

	searchKey(browser, "博客")

	time.sleep(2)
	tt = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
	browser.get_screenshot_as_file('%s.png'%(tt))

#   防止出现滚动条现象
 	js = 'document.documentElement.scrollTop=10000'
	browser.execute_script(js)

#   记录当前搜索页面
	totalInfo = []
	info = {"url":"", "con":""}
	content = browser.find_element_by_id("content_left")
	eles = content.find_elements_by_css_selector('div[class="result c-container "]')
	for ele in eles:
		tag = ele.find_element_by_tag_name('a')
		info['url'] = tag.get_attribute('href')
		info['con'] = tag.text
		totalInfo.append(info)

#   准调整到索引出来的页面
	sina = totalInfo[0]['url']
	newopen(browser, sina)
	tt = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
	browser.get_screenshot_as_file('%s.png'%(tt))

#   调整回百度搜索页面
	browser.back()
	tt = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
	browser.get_screenshot_as_file('%s.png'%(tt))
	browser.quit()
	# except:

	# 	print "error"

	# 	browser.quit()
	# 	return

if __name__ == '__main__':
	login("https://www.baidu.com/")