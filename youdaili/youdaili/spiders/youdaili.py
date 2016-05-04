#coding=utf-8

import sys
import scrapy

from scrapy.http import Request
from scrapy.spider import CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

reload(sys)
sys.setdefaultencoding('utf-8')

class daliItem(scrapy.Item):
    title = scrapy.Field()
    href = scrapy.Field()


class youdaili(CrawlSpider):
	name = "youdaili"
	allowed_domains = ["www.youdaili.net"]
	start_urls = ['http://www.youdaili.net/Daili/guonei']

	link_extractor = {
		'page':SgmlLinkExtractor(allow = 'http://www.youdaili.net/Daili/guonei/[0-9]+.html$'),
		'page_down':SgmlLinkExtractor(allow ='list_\d+.html$'),
		'sublink':SgmlLinkExtractor(allow="[0-9]_\d+.html$")
	}

	def __init__(self):
		self.lasturl = ""
		self.count = 0

	def parse(self, response):
		# get the page content
		for link in self.link_extractor['page'].extract_links(response):
			yield Request(url = link.url, callback=self.parse_desc)

		#next page
		for link in self.link_extractor['page_down'].extract_links(response):
			yield Request(url = link.url, callback=self.parse)

	def parse_desc(self, response):
		self.count += 1
		items = []
		print "@@@@@@@@@@@count:", self.count
		sel = Selector(response)
		sites = sel.xpath('//div[@class="cont_font"]/p')
		for site in sites:
			iporxys = site.xpath('//text()').extract()
			for iproxy in iporxys:
				iproxy = iproxy.strip('\r\n')
				#zhejiang
				pos = iproxy.find(u'\u6d59\u6c5f')
				#jiangsu
				pos += iproxy.find(u'\u6c5f\u82cf')
				if pos < 0:
					continue
				pos = iproxy.find("@")
				if pos < 0:
					continue
				line = iproxy[:pos]
				items.append(line+'\n')

		file = open("iproxy.txt", "a+")
		file.writelines(items)
		file.close()

		for link in self.link_extractor['sublink'].extract_links(response):
			if (self.lasturl != link.url):
				self.lasturl = link.url
				print 'link::', link.url
				yield Request(url = link.url, callback=self.parse_desc)
			else:
				continue
