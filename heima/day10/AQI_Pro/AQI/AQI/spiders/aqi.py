# -*- coding: utf-8 -*-
import scrapy

from AQI.items import AqiItem


class AqiSpider(scrapy.Spider):
    name = 'aqi'
    allowed_domains = ['www.aqistudy.cn']
    base_url = 'https://www.aqistudy.cn/historydata/'
    start_urls = [base_url]

    def parse(self, response):
        city_name_list = response.xpath('//div[@class="bottom"]/ul/div[2]/li/a/text()').extract()
        city_link_list = response.xpath('//div[@class="bottom"]/ul/div[2]/li/a/@href').extract()
        # print(city_name_list, city_link_list)
        for city_name, city_link in zip(city_name_list, city_link_list):
            item = AqiItem()
            # item = {}
            item['city_name'] = city_name
            city_url = self.base_url + city_link
            item['city_url'] = city_url
            # yield scrapy.FormRequest(city_url, callback=self.parse_month, meta={'aqi': item})
            yield item

    def parse_month(self, response):
        item = response.item['aqi']

        pass
