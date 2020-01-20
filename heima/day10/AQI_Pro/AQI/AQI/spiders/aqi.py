# -*- coding: utf-8 -*-
import scrapy


class AqiSpider(scrapy.Spider):
    name = 'aqi'
    allowed_domains = ['www.aqistudy.cn']
    start_urls = ['http://www.aqistudy.cn/historydata/']

    def parse(self, response):


        pass
