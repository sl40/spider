# -*- coding: utf-8 -*-
import scrapy

from helper.date import Date


class FundSpider(scrapy.Spider):
    name = 'fund'
    # allowed_domains = ['fund.eastmoney.com']
    # start_urls = ['http://fund.eastmoney.com/']

    def start_requests(self):
        url = 'http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery183011010295856877361_1531217714203&fundCode=000878&pageIndex=1&pageSize=20&startDate=&endDate=&_='+Date.now().millisecond()
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
                url=url,
                method="GET",
                callback=self.parse
        )

    def parse(self, response):
        print(response.body)
        pass
