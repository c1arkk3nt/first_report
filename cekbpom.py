import scrapy

from scrapy.selector import HtmlXPathSelector
		
class BPom(scrapy.Item):
	noreg = scrapy.Field()
	product = scrapy.Field()
	registered = scrapy.Field()
	
class BPomSpider(scrapy.Spider):
	name = "cekbpom"
	start_urls = 	['http://cekbpom.pom.go.id/']
	
	def parse(self, response):
	#/01/row/100/page/1/order/4/DESC # page utk data obat saja
		next_page = response.xpath('//div[@class="menu"]/a/@href').extract_first() + '/01/row/10/page/1/order/4/DESC'
		
		#response.css('div.menu > a::attr(href)').extract_first() + '/01/row/10/page/1/order/4/DESC'   

		if next_page is not None:
			yield response.follow(next_page, self.parse_produk)
		
	def parse_produk(self, response):

		total = str(response.css('span[id="tb_total"]::text').extract_first())
		hal = str(response.xpath('//input[@id="tb_hal"]/@value').extract_first())
		pgdtl = response.xpath('//input[@id="urldtl"]/@value').extract_first()
		page = response.url
		l = page.find('/order/4/DESC')
		ppage = 1
		tot = 3 #int(total)
		nexthal = 1 #int(hal)
		
#		print page
#		print l
#		print ppage
#		print tot
#		print nexthal
#		print (tot - nexthal)
#		print page[:-(len(page)-l+1)]+str(ppage)+page[l:]
		
		while (nexthal < tot): 
			next = page[:-(len(page)-l+1)]+str(ppage)+page[l:]
			nexthal = nexthal + 1
			ppage = ppage + 1
			
			if next is not None:
				yield response.follow(next, self.parse_detail, dont_filter=True)			
			
		pass	
						
	def parse_detail(self,response):
		
#		print response.url
		
		divs = response.xpath('//td[@class="odd"]') #response.xpath('//tr/@urldetil') #
		
		items = []
		count = 0
		for div in divs:
			try:
				
				item = BPom()
				item['noreg'] = div.xpath('//tr/td[1]/text()').extract()[count] + " " + div.xpath('//tr/td[1]/div/text()').extract()[count]
				item['product'] = div.xpath('//tr/td[2]/text()').extract()[count] + " " + div.xpath('//tr/td[2]/div').extract()[count]
				item['registered'] =  div.xpath('//tr/td[3]/text()').extract()[count] + " " + div.xpath('//tr/td[3]/div/text()').extract()[count]
				count = count + 1
				items.append(item)
			except (IndexError, ValueError):
				pass
		return items
			
