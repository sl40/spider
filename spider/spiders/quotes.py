# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotesltoscrape.com']
    start_urls = ['http://quotesltoscrape.com/']

    def parse(self, response):
        print('*****************')
        print(response)
        pass
