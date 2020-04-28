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
    BASE_URL = 'https://vnexpress.net/'
    # Hash table contain category name, to create directories
    CATEGORIES = {
        'giao-duc': 'Giáo dục',
        'thoi-su': 'Thời sự',
        'kinh-doanh': 'Kinh doanh',
        'phap-luat': 'Pháp luật',
        'the-gioi': 'Thế giới',
        'oto-xe-may': 'Xe',
        'suc-khoe': 'Sức khoẻ - Y tế',
        'khoa-hoc': 'Khoa học',
        'so-hoa': ' Công nghệ',
        'giai-tri': 'Giải trí',
        'the-thao': 'Thể thao',
        'doi-song': 'Đời sống',
        'du-lich': 'Du lịch'
    }

    CATEGORIES_COUNTER = {
        'giao-duc': [0, 0],
        'thoi-su': [0, 0],
        'kinh-doanh': [0, 0],
        'phap-luat': [0, 0],
        'the-gioi': [0, 0],
        'oto-xe-may': [0, 0],
        'suc-khoe': [0, 0],
        'khoa-hoc': [0, 0],
        'so-hoa': [0, 0],
        'giai-tri': [0, 0],
        'the-thao': [0, 0],
        'doi-song': [0, 0],
        'du-lich': [0, 0],
    }

    xpaths = {
        'article_list': '//h2[@class="title_news"]/a/@href  \
            | //article[contains(@class, "item-news")]/*[contains(@class, "news")]/a[contains(@data-medium, "Item")]/@href',
        'next_page': '//a[@class="btn-page next-page "]/@href',
        'title': '//h1[@class="title-detail"]/text()',
        'description': '//p[@class="description"]/text()',
        'content': '//article[contains(@class, "fck_detail")]/p[@class="Normal" and not(@style)]/text() \
        | //article[contains(@class, "fck_detail")]/p[@class="Normal" and not(@style)]/strong',
        'author': '//p[@style="text-align:right;"]/strong/text() | //p[@class="author_mail"]/strong/text()',
        'publish_date': '//div[@class="header-content width_common"]/span[@class="date"]/text()'
    }

    name = "vnexpress"
    page_limit = None
    start_urls = []