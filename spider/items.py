# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import  Item,Field


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class QuoteItem(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()


class TmallItem(scrapy.Item):
    pass


class ProductItem(Item):
    collection = 'productions'
    price = Field()
    image = Field()
    deal = Field()
    shop = Field()
    total = Field()
