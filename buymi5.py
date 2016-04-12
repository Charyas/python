#coding=utf-8

import time
import requests
import cookielib

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

user_agent = (
	'Mozilla/5.0 (Windows NT 6.1; WOW64) '+
	'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')

def savecookie(url):
	jar = cookielib.LWPCookieJar('cookie.txt')

	try:
		jar.load(ignore_discard=True)
	except:
		print "aaaaa"
		pass

	s = requests.Session()
	s.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
	s.cookies = jar

	r = s.get(url)

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap['phantomjs.page.settings.userAgent'] = user_agent
browser = webdriver.PhantomJS(executable_path="phantomjs.exe", desired_capabilities=dcap)
def login(username, passward):
	#browser.get('https://account.xiaomi.com')
	#WebDriverWait(browser, 7)

	inusename = browser.find_element_by_name("user")
	inusename.send_keys(username)
	inpasswd = browser.find_element_by_name("pwd")
	inpasswd.send_keys(passward)

	#browser.get_screenshot_as_file('aaa.png')

	currentlogin = browser.find_element_by_id("login-button")
	currentlogin.click()
	currentlogin.submit()
	time.sleep(10)
	#browser.get_screenshot_as_file('bbbb.png')

def choosedemo():
	high = browser.find_element_by_xpath('//*[@id="J_proStep"]/div[1]/ul/li[2]')
	high.click()
	color = browser.find_element_by_xpath('//*[@id="J_proStep"]/div[2]/ul/li[2]')
	color.click()
	time.sleep(3)
	browser.get_screenshot_as_file('2222.png')

def catnext():
	lost = browser.find_element_by_xpath('//*[@id="J_chooseResult"]/a')
	if lost == None:
		print "less"
		return False

	package = browser.find_element_by_xpath('//*[@id="J_choosePackage"]/ul/li[1]')
	package.click()
	return True

def choosepack():
	chaocan = browser.find_element_by_xpath('//*[@id="J_choosePackage"]/ul/li[1]')
	browser.get_screenshot_as_file('xxxxx.png')
	if chaocan == None:
		return False
	chaocan.click()

	next = browser.find_element_by_xpath('//*[@id="J_chooseResultInit"]/a')
	next.click()

def buymi5():
	browser.get('http://item.mi.com/buyphone/mi5')
	WebDriverWait(browser, 30)
	loginput = browser.find_element_by_class_name('link')
	browser.get_screenshot_as_file('1111.png')
	loginput.click()
	login("你的帐号", "对应密码")
	choosedemo()
	if catnext() == True:
		while (1):
			print "aaa"
			choosepack()

if __name__ == '__main__':
	buymi5()
