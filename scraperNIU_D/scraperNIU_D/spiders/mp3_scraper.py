# -*- coding: utf-8 -*-
import scrapy
from scrapy			import Selector
from scrapy.http	import Request


class Mp3ScraperSpider(scrapy.Spider):
	name = "mp3_scraper"
	allowed_domains = ["ondalasuperestacion.com"]
	start_urls = (
		'http://ondalasuperestacion.com/category/categorias-principal/micros-categorias-principal/insolito-universo/',
	)

	def __init__(self):
		self._1stpage = True
		self.postList = list()
		pass

	def parse(self, response):
		hxs = Selector(response)
		base = hxs.xpath('//section[@id="ContinentWrapper"]')

		# if is the 1st time of the scraper, scrap the banner
		if self._1stpage is True:
			
			self._1stpage = False
			url = base.xpath('.//section[@class="col-xs-12"]//a/@href')
			# print("********************************")
			self.postList.append( url.extract() )

		urls = base.xpath('.//section[@class="col-xs-12 col-sm-12 col-md-8 col-lg-8"]//a/@href')

		self.postList += urls.extract()
		print( len(self.postList) )
		
