# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 09:22:25 2020

@author: tuan_blade
"""


# -*- coding: utf-8 -*-
# import scrapy


# class VnexpSpider(scrapy.Spider):
#     name = 'vnexp'
#     allowed_domains = ['https://vnexpress.net/']
#     start_urls = ['http://https://vnexpress.net//']

#     def parse(self, response):
#         pass
import scrapy
import os
import re
import json
from codecs import open
from ..items import NewsCrawlerItem
from .base_spider import BaseSpider



class VnExpress(BaseSpider):
    BASE_URL = 'http://baolongan.vn/'
    # Hash table contain category name, to create directories
    CATEGORIES = {
        'thoi-su-chinh-tri': 'Thời sự-Chính trị',
        'phap-luat': 'Pháp luật',
        'kinh-te':'Kinh Tế',
        'doi-song-xa-hoi':'Xã hội',
        'quoc-phong-an-ninh':'QP-AN'
        
    }

    CATEGORIES_COUNTER = {
        'thoi-su-chinh-tri': [0, 0],        
        'phap-luat': [0, 0],
        'kinh-te':[0, 0],
        'doi-song-xa-hoi':[0, 0],
        'quoc-phong-an-ninh':[0, 0]
    }

    xpaths = {
        'article_list':'//h2[@class="h2cate"]/a/@href|//div[@class="boxtinmoi"]//li//a[1]/@href',
        'next_page': '//div[@class="fright"]//a[contains(text(),">")]/@href',
        'title': '//h1[@class="margintopbot10 fw600"]/text()',
        'description': '//p[@class="fontd"]/text()',
        'content': '//div[@class="content-fck slider-jsgallery"]//p/text()',
        'author': '//p[@style="text-align: right;"]//strong/text()',
        'publish_date': '//span[@class="pubdate"]/text()'
    }

    name = "baolongan"
    page_limit = None
    start_urls = []