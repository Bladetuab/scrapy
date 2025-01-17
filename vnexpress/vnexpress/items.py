# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()
    classification = scrapy.Field()
    sentiment = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    publish_date = scrapy.Field()

