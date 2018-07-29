# -*- coding: utf-8 -*-
import scrapy


class FundSummary(scrapy.Spider):
    name = 'fundSummary'
    allowed_domains = ['http://fund.eastmoney.com']
    start_urls = ['http://fund.eastmoney.com/fund.html#os_1;isall_0;ft_;pt_1']

    def parse(self, response):
        print('*****************')
        print(response)
        pass
