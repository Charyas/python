#coding=utf-8

import mechanize

def viewPage(url):
	browser = mechanize.Browser()
	page = browser.open(url)
	source_code = page.read()
	print source_code
viewPage("www.baidu.com")