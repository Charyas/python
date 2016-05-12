import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.selector import Selector

from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging

from utilities import mycsv, scripts, converter
import pprint
import re, demjson, unicodecsv


csv_dict = {}

class SB_X(CrawlSpider):
		name = 'xxx'
		start_urls = ['http://www.amazon.com/s/ref=sr_in_c_p_89_705?fst=as%3Aoff&rh=n%3A7141123011%2Ck%3At-shirt%2Cp_89%3ACharles+Amelia&bbn=7141123011&keywords=t-shirt&ie=UTF8&qid=1462936373&rnid=2528832011',]

		rules = (
				Rule (LinkExtractor(allow=(),restrict_xpaths=('//span[@class="pagnLink"]',)), follow= True),
				Rule (LinkExtractor(allow=(),restrict_xpaths=('//a[@class="a-link-normal s-access-detail-page  a-text-normal"]',)), 
					callback="parse_category" , follow= True),)

		# def parse(self, response):
		def parse_category(self, response):						

			sel = Selector(response)
			product_name = sel.xpath("//span[@id='productTitle']/text()").extract()[0]						
			parent_asin = sel.xpath("//div[@id='tell-a-friend']/@data-dest").extract()[0].split('parentASIN=')[-1].split('&')[0]						
			try:
				price  = sel.xpath("//span[@id='priceblock_ourprice']/text()").extract()[0].replace('$','')	
				price = converter.cleanup_price(price)
			except:
				price = ''
			
			try:
				brand = sel.xpath("//a[@id='brand']/text()").extract()[0]
			except:
				brand =  sel.xpath("//a[@id='brand']/@href").extract()[0].split("/")[1]

			parent_row = ['Product', parent_asin, brand, product_name,'',price]
			
			global csv_dict
			csv_dict[parent_asin] = {}
			csv_dict[parent_asin]['Parent_Row'] = parent_row
			# mywriter.writerow(row)

			size_script = sel.xpath("//script[@language='JavaScript'][contains(text(),'window.isTwisterAUI = 1')]").extract()[0]
			color_script = sel.xpath("//script[@type='text/javascript'][contains(text(),'customerImages')]").extract()[0]
					
			'''
			Initializing Dictionaries for Variants(Asin, Variant Values), Pricing(Asin, Price) and Images(Asin, Images)
			'''
			variant_dict, price_dict, image_dict= {}, {}, {}

			size_script = size_script.split('dimensionValuesDisplayData')[-1].split('"deviceType')[0]
			new_script = re.findall('"(.*?)]',size_script.split("hidePopover")[0])

			for i in new_script:
				asin = i.split('[')[0].replace(':{"','').replace('":','')				
				variants = i.split('["')[-1]
				variant_dict[asin] = variants		

			color_script = color_script.split('data["colorImages"] =')[-1].split('data["heroImage"] = {};')[0].rsplit(';',1)[0]		
			color_script = demjson.decode(color_script)

			for key,value in variant_dict.iteritems():
				try:
					color = value.split('"')[-2].split('"')[0]					
					image_dict[color] = []
					
					for images in color_script[color]:					
						image_dict[color].append(images['large'])	
				except:
					pass
		

			price_url = sel.xpath("//script[contains(text(),'immutableURL')]/text()").extract()[0].split('immutableURLPrefix":"')[-1].split('"')[0]
			price_url = 'http://www.amazon.com' + price_url + '&psc=1&isFlushing=2&dpEnvironment=softlines&mType=full'

			'''
			To check if Swatches exist
			'''
			
			swatches  = response.xpath( "//div[@id='variation_style_name']//li[contains(@id,'style')]")
			if swatches:				
				for swatch in swatches:
					swatch_price = swatch.xpath(".//div[@class='twisterSlotDiv']//span[@class='a-size-mini']/text()").extract()					
					if swatch_price:
						swatch_price = swatch_price[0].replace('$','').strip()
						swatch_price = converter.cleanup_price(swatch_price)

					else:
						swatch_price = False
					swatch_asin = swatch.xpath("@data-dp-url").extract()[0].split('dp/')[-1].split('/')[0]					
					price_dict[swatch_asin] = swatch_price

			self.variant_dict = variant_dict

			for asin, variants in variant_dict.iteritems():	
				row = []
				color =  variants.split('"')[-2]				
				size  = variants.split('"')[0]
				
				# # print url
				# if asin in price_dict:
				# 	variant_price = price_dict[asin]					
				# 	if variant_price == False:
				# 		continue									
				# else:
				# 	variant_price = price

				# row = ['SKU', asin, '', color, size, variant_price , '', '']

				row = ['SKU', asin, '', color, size,'', '11','80' , 'a','2',]
				for image in image_dict[color]:
					row.append(image)			
								
				'''
				# Generating Requests for Price Ajax Script
				'''
				url = price_url + '&asinList=%s&id=%s' %(asin,asin)

				__price_request = Request(url, callback = self.parse_price)
				__price_request.meta['row'] = row
				__price_request.meta['parent_asin'] = parent_asin
				yield __price_request

				# break

				
		def parse_price(self, response):			

			csv_row = response.meta['row']		
			parent_asin = response.meta['parent_asin']	

			if 'a-size-medium a-color-price\\">' in response.body:
				ajax_price = response.body.split('a-size-medium a-color-price\\">')[-1].split('<\/')[0].replace('$','')
				ajax_price = re.findall(r'\d+',ajax_price)[0]
				csv_row[5] = converter.cleanup_price(ajax_price)				
				child_asin = csv_row[1]
				csv_dict[parent_asin][csv_row[1]] = csv_row

if __name__ == '__main__':
		
		process = CrawlerProcess()										
		process.crawl(SB_X)
		process.start()				
		
		mywriter = mycsv.initialize_csv('SB_X.csv')
		

		for parent_asin, child_dicts in csv_dict.iteritems():
			mywriter.writerow(child_dicts['Parent_Row'])			
			del child_dicts['Parent_Row']

			for child_asin, values in child_dicts.iteritems():
				if values[5] != '':
					mywriter.writerow(values)