# -*- coding: utf-8 -*-
import scrapy
from scrapy			import Selector
from scrapy.http	import Request
import urlparse

class Mp3ScraperSpider(scrapy.Spider):
	name = "mp3_scraper"
	allowed_domains = ["ondalasuperestacion.com"]
	start_urls = (
		'http://ondalasuperestacion.com/category/categorias-principal/micros-categorias-principal/insolito-universo/',
	)

	def __init__(self):
		self._1stpage = True
		self.postList = list()
		self.audioList = list()
		pass

	def parse(self, response):
		hxs = Selector(response)
		base = hxs.xpath('//section[@id="ContinentWrapper"]')

		# if is the 1st time of the scraper, scrap the banner
		if self._1stpage is True:
			
			self._1stpage = False
			url = base.xpath('.//section[@class="col-xs-12"]//a/@href')
			# print("********************************")
			self.postList.append( url.extract()[0] )

		urls = base.xpath('.//section[@class="col-xs-12 col-sm-12 col-md-8 col-lg-8"]//a/@href')

		self.postList += urls.extract()

		for url in self.postList:
			# print(url)
			url = response.urljoin( str(url) )
			# print(url)
			yield Request( url, callback=self.parse_post )

	def parse_post(self, response):
		hxs = Selector(response)
		# audioUrl = hxs.xpath('//audio/@src').extract()
		playerUrl = hxs.xpath('//iframe/@src').extract()[0]
		# playerUrl = response.urljoin( str(playerUrl) )

		parsed = urlparse.urlparse(playerUrl)
		mp3Url = urlparse.parse_qs(parsed.query)['audioid']
		
		print(mp3Url)
		print("----------------")