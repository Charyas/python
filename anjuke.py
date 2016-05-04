#codeing=utf-8

import requests
url = 'http://shanghai.anjuke.com/community/'

def getAnjuke(url):
	# 每条目录对应的 标题与连接地址
	subinfo = {'title':"", 'desturl':""}

	#返回当前页面的所有条目 和下一页
	info = {'listname':[], 'next':""}
	headers = {
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate, sdch',
		'Accept-Language':'en-US,en;q=0.8,zh;q=0.6',
		'Connection':'keep-alive',
		'Host':'shanghai.anjuke.com',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
	}

	r = requests.get(url, headers=headers)
	# parser

	# 这里没有用正则弄，可以考虑下
	pos1 = r.content.find('<a class="light" rel="nofollow"  href="http://shanghai.anjuke.com/community/o4/"')
	pos2 = r.content.find('<div class="page-content">')
	content = r.content[pos1:pos2]

# 抓取关键字段 link 和 title 并记录
	while 1:
		pos = content.find('link="')
		if pos < 0:
			break
		content= content[pos + len('link="'):]
		pos = content.find('"')
		subinfo['desturl']= "http://shanghai.anjuke.com" + content[:pos]
		pos = content.find('title="')
		content=content[pos + len('title="'):]
		pos = content.find('"')
		# 需要转码，这个地方没有弄 TODO:
		subinfo['title']=content[:pos]
		info['listname'].append(subinfo)


	pos3 = r.content.find('class="aNxt">')
	nextpage = r.content[pos3-50:pos3]
	pos = nextpage.find('http://')
	info['next'] = nextpage[pos:len(nextpage)-2]

	return info

# 获取“东郊紫园”
def getdetail(url):
	headers = {
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate, sdch',
		'Accept-Language':'en-US,en;q=0.8,zh;q=0.6',
		'Connection':'keep-alive',
		'Host':'shanghai.anjuke.com',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
	}
	r = requests.get(url, headers=headers)
	print r.content
	# 解析对应的数据 TODO:

if __name__ == '__main__':
	listname = getAnjuke(url)
	print listname
	# 这里需要添加循环根据 listname['next']的特征值访问下一页