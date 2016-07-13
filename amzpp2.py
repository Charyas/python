#!/usr/bin/env python
#encoding: utf-8
# geebook.net
#06.06.16
#主題:
#備忘:用于翻页
######################
import sys, os, os.path
import re
reload(sys)
import codecs
from bs4 import BeautifulSoup
sys.setdefaultencoding("utf-8")
import requests
import random
#url = sys.argv[1]


def detail(url):
	print ("=>"+url)

	r = requests.get(url,headers=headers)
	soup = BeautifulSoup(r.content, 'lxml')
	try:
		rank = re.findall(b'\#\d+\ in\ Clothing',r.content)[0]
	except:
		rank ="无排名"
	try:
		price=list(set(re.findall(b"\$\d\d\.\d\d\ \-\ \$\d\d.\d\d",r.content)))[0]
	except:
		#修改过的地方1
		try:
			price=list(set(re.findall(b"\$\d\d",r.content)))[0]
		except:
			price="unknow"

	try:
		for i in soup.select('span.a-size-base.a-color-base'):
			ship=i.text
	except:
		ship = 'Free'

	try:
		for item in str(soup.select('script')).split(']},"hidePopover":0,"disableJsInteraction')[0].split('"dimensionValuesDisplayData":{')[1].replace('[','尺寸:').split('],'):
			result.append(item.replace(',','|颜色:').replace('|',',价格:'+str(price).replace(' - ','至'))+',运费'+str(ship)+',Rank:'+str(rank))
	except:
		next

def asin(url):
	print ("asin=>"+url)
	return list(set(re.findall(b"B0[A-Z0-9]{8}",requests.get(url,headers = headers).content)))

def gather(soup):
	for i in soup.findAll(id='pagn'):
		maxpage = re.findall("\d+",i.text)[-1]
		for p in range(1,int(maxpage)+1):
			urls.append(what.replace('&page=','')+'&page=%s' % (p))
		print ("網址收集完畢<=")

def soup(url):
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:19.0)\Gecko/10100101 Firefox/19.0'}
	r = requests.get(url,headers=headers)
	soup = BeautifulSoup(r.content, 'lxml')
	return soup


#https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=toy
#http://www.amazon.com/Melissa-Doug-Deluxe-Pounding-Bench/dp/B004NCEL4M?ie=UTF8&keywords=toy&qid=1465307082&ref_=sr_1_1&refinements=p_89%3AMelissa%20%26%20Doug&sr=8-1
#这个 运行之前，要给一个参数，代表url从那个文件读取。你那里有么？在桌面吧？
#urlpath=sys.argv[1]

urlpath=raw_input("输入URL")
#urlpath='/Users/zhengjunli/Desktop/amzc/url'
print '开始读取url：'+urlpath
starturls=[]
urls=[]

result=[]
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:19.0)\Gecko/10100101 Firefox/19.0'}
startfile=open(urlpath, 'r')
for uu in startfile.readlines():
	starturls.append(uu)
    #gather(soup(uu))

print("=>"+str(len(starturls)))

# 收集每一页的url
for what in starturls:
	gather(soup(what))

print ("==>asin收集")
#收集每页url中的具体内容
for i in urls:
	for a in asin(urls[0]):
		print('当前个数:'+str(len(result)))
		detail('https://www.amazon.com/dp/'+str(a,encoding="utf-8"))

print ("采集完毕正在写入文档")
print (str(len(result)))

# 数据保存路径
f=open('/Users/zhengjunli/Desktop/'+str(random.randint(100000,10000000))+'data.csv', 'w')
f.writelines(result)
print ("本次采集结束")