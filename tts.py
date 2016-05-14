#coding=utf-8
#
import urllib
import requests
import json
import sys
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')

def tts(key):
	code = urllib.quote(str(key))
	url = 'https://cache-a.oddcast.com/tts/gen.php?EID=3&LID=10&VID=1&TXT=' + code + '&IS_UTF8=1&ACC=3314795&API=2292375&CB=vw_mc.vwCallback'

	headers = {
		'Accept':'*/*',
		'Accept-Encoding':'gzip, deflate, sdch',
		'Accept-Language':'en-US,en;q=0.8,zh;q=0.6',
		'Connection':'keep-alive',
		'Host':'cache-a.oddcast.com',
		'Referer':'https://www.vocalware.com/index/demo',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
	}

	data = {
		'EID':'3',
		'LID':'10',
		'VID':'1',
		'TXT':code,
		'IS_UTF8':'1',
		'ACC':'3314795',
		'API':'2292375',
		'CB':'vw_mc.vwCallback'
	}

	r = requests.get(url, headers=headers, data=data, verify=False)
	content = r.text
	content = content.strip('vw_mc.vwCallback(')
	content = content.strip(')')
	print content
	jsdata = json.loads(content)

	headers = {
		'Accept-Encoding':'identity;q=1, *;q=0',
		'Range':'bytes=0-',
		'Referer':'https://www.vocalware.com/index/demo',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
	}
	r = requests.get(jsdata['URL'], headers = headers, verify=False)

	tt = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
	file = open('%s.mp3'%(tt), 'wb')
	file.write(r.content)
	file.close()

import chardet
if __name__ == '__main__':
	world = sys.argv[1]
	tts(world.decode('gb2312').encode('utf-8'))