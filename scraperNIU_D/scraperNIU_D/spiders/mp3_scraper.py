# -*- coding: utf-8 -*-
import scrapy
from scrapy				import Selector
from scrapy.http		import Request
from scraperNIU_D.items	import audioItem
import urlparse


class Mp3ScraperSpider(scrapy.Spider):
	name = "mp3_scraper"
	allowed_domains = ["ondalasuperestacion.com"]
	start_urls = (
		# 'http://ondalasuperestacion.com/category/categorias-principal/micros-categorias-principal/insolito-universo/',
		'http://ondalasuperestacion.com/category/categorias-principal/micros-categorias-principal/insolito-universo/page/2/'
	)

	def __init__(self):
		self._1stpage = True

	def parse(self, response):
		postList = list()

		hxs = Selector(response)
		base = hxs.xpath('//section[@id="ContinentWrapper"]')

		# if is the 1st time of the scraper, scrap the banner
		if self._1stpage is True:
			
			self._1stpage = False
			url = base.xpath('.//section[@class="col-xs-12"]//a/@href')
			# print("********************************")
			postList.append( url.extract()[0] )

		urls = base.xpath('.//section[@class="col-xs-12 col-sm-12 col-md-8 col-lg-8"]//a/@href')

		postList += urls.extract()

		for url in postList:
			# print(url)
			url = response.urljoin( str(url) )
			# print(url)
			# yield Request( url, callback=self.parse_post )

		# the next links ->
		# nextlink = base.xpath('./section/div[@class="row"][2]/div[@class="col-xs-1 navlinks"]//a').extract()
		# print( len(nextlink) )


	def parse_post(self, response):
		hxs = Selector(response)

		playerUrl = hxs.xpath('//iframe/@src').extract()
		title = hxs.xpath('//article[@class="background-white"]//h2/text()').extract()[0]

		if len(playerUrl) is 0:
			print("---------------------")
			print("No audio for: "+title)
			print("---------------------")
			return
		else:
			playerUrl = playerUrl[0]

		parsed = urlparse.urlparse(playerUrl)
		mp3Url = urlparse.parse_qs(parsed.query)['audioid']

		item = audioItem()
		item['url']		= mp3Url
		item['title']	= title
		yield item
