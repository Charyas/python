#coding=utf-8
import os
import sys
from os import path

import json
import imghdr
import base64
import requests
import time, datetime

from uuPythonDemo import *
#from uuLinux import *
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

def post_captcha(serial, guess, captcha_id, proxy=None):
	url = "https://fmipalcweb.icloud.com/fmipalcservice/client/checkActivationLock"
	payload = {"deviceId":serial, 'captchaCode':guess, 'captchaContext':{'id':str(captcha_id)}}

	headers = {
		'Accept':'*/*',
		'Accept-Encoding':'gzip, deflate',
		'Accept-Language':'en-US,en;q=0.8,zh;q=0.6',
		'Connection':'keep-alive',
		'Content-Length':'1019',
		'Content-Type':'text/plain',
		'Host':'fmipalcweb.icloud.com',
		'Origin':'https://www.icloud.com',
		'Referer':'https://www.icloud.com/activationlock/',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
	}

	#verity = "/etc/ssl/certs/ca-certificates.crt"
	r = requests.post(url, data=json.dumps(payload),headers=headers, verify=False)
	return r.json()

def get_captcha():
	rnd = jsGettime()
	url = 'https://fmipalcweb.icloud.com/fmipalcservice/client/getCaptchaImage?rnd=' + rnd

	headers = {
		'Accept':'*/*',
		'Accept-Encoding':'gzip, deflate, sdch',
		'Accept-Language':'en-US,en;q=0.8,zh;q=0.6',
		'Connection':'keep-alive',
		'Content-Type':'text/plain',
		'Host':'fmipalcweb.icloud.com',
		'Origin':'https://www.icloud.com',
		'Referer':'https://www.icloud.com/activationlock/',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
	}

	#verity = "/etc/ssl/certs/ca-certificates.crt"
	r = requests.get(url, headers=headers, verify=False)

	try:
		response = r.json()
		requestURL = response['image']
		id = response['captchaContext']['id']

		return {'requestURL': requestURL, 'id':id}
	except:
		print "SERVICE UNAVAILABLE"

def jsGettime():
	rnd = datetime.datetime.now()
	t = str(int(time.mktime(rnd.timetuple())))
	ms = str(int(rnd.microsecond * 0.001))

	return t + ms

# decode pic
def decode2pic(content, file_name='test'):
	npos = content.index(',')
	b64_data = content[npos+1:]
	image_data = base64.b64decode(b64_data)
	image_type = imghdr.what('', image_data)

	destination_file_name = file_name + '.' + image_type

	destination = open(destination_file_name, 'wb')
	destination.write(image_data)
	destination.close()
	return destination_file_name

def main(imei):
	for i in range(3):
		res = get_captcha()
		filename = r"test_pics/"+"test_%s"%i
		pic_name = decode2pic(res['requestURL'], filename)
		#code = check_out(pic_name)
		code = look_result(pic_name)
		print code

		con = res['id']
		response = post_captcha(imei, code, con)
		if response['statusCode'] == '200':
			ret = "ActiveLock:" + str(response['locked'])
			return ret
		else:
			continue
	return "ERROR"

if __name__ == '__main__':
	imei = sys.argv[1]
	if len(imei) != 15:
		print "error:imei len"
	print main(imei)
