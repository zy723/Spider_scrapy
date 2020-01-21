# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AqiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city_name = scrapy.Field()  # 城市名字
    date = scrapy.Field()  # 日期
    aqi = scrapy.Field()  # AQI
    level = scrapy.Field()  # 质量级别
    pm2_5 = scrapy.Field()  # PM2.5
    pm10 = scrapy.Field()  # PM10
    so_2 = scrapy.Field()  # SO2
    co = scrapy.Field()  # CO
    no_2 = scrapy.Field()  # NO2
    o3 = scrapy.Field()  # Q3

    crawl_time = scrapy.Field()  # 抓取时间
    spider = scrapy.Field()  # 爬虫名字
    city_url = scrapy.Field()  # 爬虫名字
