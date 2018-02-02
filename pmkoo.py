#coding=utf-8
import os
import time
import json
import requests
from multiprocessing import Process, Queue, Pool

def download_info():
	page = 1
	while True:
		page_json = download_page(page)
		if not page_json['data']['list']:
			break
		save_page(page_json)
		page += 1

def download_page(page):
	url = 'http://api.pmkoo.cn/aiss/suite/suiteList.do'
	params = {'page':page, 'userId':153044}

	rsp = requests.post(url, data=params)
	return rsp.json()

def save_page(page_json):
	txt = json.dumps(page_json)
	with open('data/info.txt', 'a') as f:
		f.write(txt)
		f.write('\n')

def get_info():
	res = []
	with open('data/info.txt', 'r') as f:
		for line in f:
			data = json.loads(line)
			res.append(data['data']['list'])
	return res

def get_info_imgs(info):
	res = []
	for items in info:
		for item in items:
			nickname = item['author']['nickname']
			catalog = item['source']['catalog']
			name = item['source']['name']
			issue = item['issue']
			pictureCount = item['pictureCount']
			for pix_idx in range(pictureCount):
				url = "http://com-pmkoo-img.oss-cn-beijing.aliyuncs.com/picture/%s/%s/%s.jpg" % (catalog, issue, pix_idx)
				directory = os.path.join('data', name, '%s-%s' % (issue, nickname))
				filepath = os.path.join(directory, "%s.jpg" % pix_idx)
				res.append((url, directory, filepath))
	return res

def setup_download_dir(directory):
	if not os.path.exists(directory):
		try:
			os.makedirs(directory)
		except Exception as e:
			pass
	return True

def download_one(img):
	url, directory, filepath = img
	if os.path.exists(filepath):
		print ('exists:', filepath)
		return

	headers = {
		"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
	}

	setup_download_dir(directory)
	rsp = requests.get(url, headers=headers)
	print 'start download:', url
	with open(filepath, 'wb') as f:
		f.write(rsp.content)
		print 'end download', url

def download(imgs, processes=10):
	start_time = time.time()
	pool = Pool(processes)
	for img in imgs:
		pool.apply_async(download_one, (img, ))
	pool.close()
	pool.join()
	end_time = time.time()
	print 'using %s mins download over!!' %(end_time - start_time)


if __name__ == '__main__':
	#download_info()

	info = get_info()

	imgs = get_info_imgs(info)
	print len(imgs)
	download(imgs)