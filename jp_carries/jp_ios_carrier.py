#coding=utf-8
import os
import time, datetime
import requests
import json
import base64
import imghdr
import subprocess
import random
from PIL import Image
from numpy import *

import platform
from PIL import Image

from uuPythonDemo import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def cut_image(file_name):
	img = Image.open(file_name)
	w, h = img.size
	box = (w/4, h/5+50, w/4+300, h/5 +100)
	roi = img.crop(box)
	if os.path.isfile('capcha.png'):
		os.remove("capcha.png")
	roi.save("capcha.png")

def reg_pic(file_name):
	code = look_result(file_name)
	return code

def get_ntt_captcha(imei):
	user_agent = (
		'Mozilla/5.0 (Windows NT 6.1; WOW64) '+
		'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')

	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap['phantomjs.page.settings.userAgent'] = user_agent

	system_name = platform.system()
	if system_name == "Windows":
		browser = webdriver.PhantomJS(executable_path="phantomjs.exe", desired_capabilities=dcap)
	else:
		browser = webdriver.PhantomJS(executable_path="./phantomjs",desired_capabilities=dcap)

	browser.get('http://nw-restriction.nttdocomo.co.jp/search.php')
	WebDriverWait(browser, 7)
	enter_search = browser.find_element_by_class_name("btntotop")
	enter_search.click()
	WebDriverWait(browser, 60)
	browser.save_screenshot("whole.png")
	time.sleep(3)
	browser.save_screenshot("whole.png")
	cut_image("whole.png")
	code = reg_pic('capcha.png')

	input_object = browser.find_element_by_name("productno")
	input_object.send_keys(imei)
	input_capcha = browser.find_element_by_name("attestationkey")
	input_capcha.send_keys(code)

	button_click = browser.find_element_by_class_name("btn1")
	button_click.submit()
	browser.save_screenshot("hehehe.png")
	out_put = browser.page_source
	pos = out_put.find("width:250px; display:inline-block; font-size: 3em; padding: 4px; border: 2px solid #CC0033;")
	pos = pos + len("width:250px; display:inline-block; font-size: 3em; padding: 4px; border: 2px solid #CC0033;")
	newline = out_put[pos: pos + 10]
	#print newline
	ret = ''
	pos = newline.find("-")
	if pos >= 0:
		ret = ''
	else:
		ret = "DOCOMO"
	browser.quit()
	return ret

def post_au(imei):
	user_agent = (
		'Mozilla/5.0 (Windows NT 6.1; WOW64) '+
		'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')

	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap['phantomjs.page.settings.userAgent'] = user_agent

	system_name = platform.system()
	if system_name == "Windows":
		browser = webdriver.PhantomJS(executable_path="phantomjs.exe", desired_capabilities=dcap)
	else:
		browser = webdriver.PhantomJS(executable_path="./phantomjs",desired_capabilities=dcap)

	browser.get('https://au-cs0.kddi.com/FtHome')
	WebDriverWait(browser, 3)
	input_object = browser.find_element_by_name("IMEI")
	input_object.send_keys(imei)

	button_click = browser.find_element_by_id("btCenter")
	button_click.submit()
	time.sleep(1)

	ret = ''
	stat = ''

	ele_stat = browser.find_element_by_xpath('//*[@id="innerBox"]/div[2]/div[2]/div')
	if ele_stat.text != u'\uff0d':
		ret = "KDDI"
		if ele_stat.text == "○":
			print('1')
			stat = 'normal'

		if ele_stat.text == "▲":
			print('2')
			stat = 'limit'

		if ele_stat.text == "×":
			print('3')
			stat = 'disable'

	browser.quit()
	return (ret,stat)

def post_softbank(imei):
	url = "https://ct11.my.softbank.jp/WBF/icv?lbk=14"
	data = {'_PageID':'WBF001000', '_DataStoreID':'DSWBF100Control', '_ControlID':'WBF100Control',
			'_ActionID':'TE001','imei':imei,'ACT_TE001':'+%E7%A2%BA+%E8%AA%8D+'}

	headers = {
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate',
		'Accept-Language':'en-US,en;q=0.8,zh;q=0.6',
		'Connection':'keep-alive',
		'Content-Length':'140',
		'Host':'ct11.my.softbank.jp',
		'Origin':'https://ct11.my.softbank.jp',
		'Referer':'https://ct11.my.softbank.jp/WBF/icv',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
	}

	r = requests.post(url, data,headers=headers)
	data = r.text
	ret = ''
	stat =''

	pos = data.find('<font size="8" color="#666666"')
	if pos >= 0:
		text = data[pos:pos + 80]
		pos = text.find(u'\uff0d')
		if pos < 0:
			ret = "SOFTBANK"
			if text.find("×") >= 0:
				stat = "disable"
			if text.find("○") >= 0:
				stat = "normal"
			if text.find("▲") >= 0:
				stat= "limit"

	return (ret,stat)

# def check_op(imei):
# 	softbank = post_softbank(imei)
# 	if softbank == "SOFTBANK": return softbank
# 	kddi = post_au(imei)
# 	if kddi == "KDDI": return kddi
# 	docomo = get_ntt_captcha(imei)
# 	if docomo == "DOCOMO": return docomo

# 	return "UNKNOW"

if __name__ == '__main__':
	# softbank = post_softbank("358542050067973")
	# print(softbank)
	# print(post_au('990002234529798'))
	# print(post_au('358805050661610'))
	get_ntt_captcha('354376063893610')