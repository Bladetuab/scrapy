# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 10:53:27 2020

@author: tuan_blade
"""


# -*- coding: utf8 -*-
import scrapy
import os
import re
import json
from codecs import open
from urllib import parse
from scrapy.spiders import CrawlSpider, Rule
from vnexpress.items import NewsCrawlerItem


class BaseSpider(CrawlSpider):
    name = None
    allowed_domains = {}
    BASE_URL = None
    # Hash table contain category name, to create directories
    CATEGORIES = {}
    CATEGORIES_COUNTER = {}
    xpaths = {}
    rules = {}

    ''' For example:
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
    } '''
    # No need to change
    page_limit = None
    start_urls = []

    def __init__(self, category=None, limit=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if limit != None:
            self.page_limit = int(limit)

        if category in self.CATEGORIES: # if a category arg is passed
            self.start_urls = [self.BASE_URL + category]
        else:
            for CATEGORY in self.CATEGORIES: # Iterating Through Keys 
                self.start_urls.append(self.BASE_URL + CATEGORY)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_list_news)

    def parse_list_news(self, response):
        category = self.get_category_from_url(response.url)
        
        if (self.page_limit is not None) and (self.CATEGORIES_COUNTER[category][1] >= self.page_limit or self.page_limit <= 0):
            return
        
        next_page_url = self.extract_next_page_url(response)

        if category in self.CATEGORIES and next_page_url is not None:
            self.CATEGORIES_COUNTER[category][1] = self.CATEGORIES_COUNTER[category][1] + 1
            # Recursion to crawl next page
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse_list_news)
        else:
            return

        # Process
        list_new_urls = response.xpath(self.xpaths['article_list']).getall()
        for url in list_new_urls:
            url = parse.urljoin(self.BASE_URL, url)
            yield scrapy.Request(url=url, callback=self.parse_news, meta= {'category': self.CATEGORIES[category]})
        

    # Need to change----------------------------------
    def parse_news(self, response):
        article = NewsCrawlerItem()
        article['link'] = response.url
        article['category'] = response.meta.get('category')
        article['classification'] = None
        article['sentiment'] = None

        title = response.xpath(self.xpaths['title']).get()
        if title != None:
            article['title'] = title.strip()
        else:
            article['title'] = title

        description = response.xpath(self.xpaths['description']).get()
        if description != None:
            article['description'] = title.strip()
        else:
            article['description'] = description

        content_list = response.xpath(self.xpaths['content']).getall()
        content = ''
        for p in content_list:
            content += p
        article['content'] = content.strip()

        arthor = response.xpath(self.xpaths['author']).get()
        if arthor != None:
            article['author'] = arthor.strip()
        else:
            article['author'] = arthor

        date = response.xpath(self.xpaths['publish_date']).get()
        if date != None:
            article['publish_date'] = date.strip()
        else:
            article['publish_date'] = date
        
        yield article


    def extract_next_page_url(self, response):
        # Get link of next page
        url = response.xpath(self.xpaths['next_page']).get()
        if self.BASE_URL in url:
            next_page_url = url
        else:
            next_page_url = parse.urljoin(self.BASE_URL, url[1:])
        return next_page_url


    def get_category_from_url(self,url):
        # etc: "https://vnexpress.net/the-gioi" ==> the-gioi
        items = url.split('/')
        category = None
        if len(items) >= 4:
            category = re.sub(r'-p[0-9]+', '', items[3])
        return category
