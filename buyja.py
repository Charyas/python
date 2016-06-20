#coding=utf-8
#
#
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from scrapy.crawler import CrawlerProcess


class Amazon_Spider(CrawlSpider):
	name = "amazon_spider"
	start_urls = ['http://www.amazon.com/s/ref=sr_in_c_p_89_705?fst=as%3Aoff&rh=n%3A7141123011%2Ck%3At-shirt%2Cp_89%3ACharles+Amelia&bbn=7141123011&keywords=t-shirt&ie=UTF8&qid=1462936373&rnid=2528832011',]
	rules = (
		Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//span[@class="pagnLink"]',)), follow= True),
		Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//a[@class="a-link-normal s-access-detail-page  a-text-normal"]',)), 
			callback="parse_category" , follow= True),)
	def parse_category(self, response):
		print "#####", response.url

class JD_Spider(CrawlSpider):
	name = "jd_spider"
	start_urls = ['http://search.jd.com/Search?keyword=java&enc=utf-8']

	#Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//span[@class="pagnLink"]',)), follow= True),
	rules = (Rule (SgmlLinkExtractor(allow=(),restrict_xpaths=('//a[@class="p-name"]/a',)), 
					callback="parse_item" , follow= True),)

	def parse_item(self, response):
		print "@@@@@@@@@@"
		sel = Selector(response)
		print response.url
		# item = sel.xpath('//div[@class="gl-i-wrap"]')


		# #prices = item.xpath('//div[@class="p-price"]/strong/@data-price').extract()
		# names  = item.xpath('//div/[@class="p-name"]/a/em').extract()

		# print "######", names

if __name__ == '__main__':
	# jd = CrawlerProcess()
	# jd.crawl(JD_Spider)
	# jd.start()

	amazon = CrawlerProcess()
	amazon.crawl(Amazon_Spider)
	amazon.start()

	print "###end####"