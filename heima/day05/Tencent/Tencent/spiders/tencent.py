# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TencentSpider(CrawlSpider):
    name = 'tencent'
    allowed_domains = ['www.tencent.com']
    start_urls = ['http://www.tencent.com/']

    rules = (
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # 提取链接
        Rule(LinkExtractor(allow=r'start'), follow=True),
        # 自动提取符合规则的 详情url 自动发送请求获取url列表 获取response
        Rule(LinkExtractor(allow=r'start'), callback='parse_item', follow=False),

    )

    def parse_item(self, response):
        item = {}
        item['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract_first()
        item['name'] = response.xpath('//div[@id="name"]').extract_first()
        item['description'] = response.xpath('//div[@id="description"]').extract_first()
        return item
