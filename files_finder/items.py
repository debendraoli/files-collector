# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class OpaxeItem(scrapy.Item):
    company_id = scrapy.Field()
    page_url = scrapy.Field()
    links = scrapy.Field()
    body = scrapy.Field()
