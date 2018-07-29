# -*- coding: utf-8 -*-
import scrapy


class TmallSpider(scrapy.Spider):
    name = 'tmall'
    allowed_domains = ['item.taobao.com']
    start_urls = ['https://item.taobao.com/item.htm?spm=a219r.lm874.14.1.26401b14vxfL07&id=569525368311&ns=1&abbucket=8']

    def parse(self, response):
        filename = response.url.split("/")[-2]
        print('***************************8')
        print(response.body)
        with open(filename, 'wb') as f:
            f.write(response.body)
        pass
