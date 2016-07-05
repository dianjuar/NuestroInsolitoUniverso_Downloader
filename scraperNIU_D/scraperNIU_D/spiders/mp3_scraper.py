# -*- coding: utf-8 -*-
import scrapy


class Mp3ScraperSpider(scrapy.Spider):
	name = "mp3_scraper"
	allowed_domains = ["ondalasuperestacion.com"]
	start_urls = (
		'http://ondalasuperestacion.com/category/categorias-principal/micros-categorias-principal/insolito-universo/',
	)

	def parse(self, response):
		# hxs = Selector(response)
		pass