# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from scrapy.exporters import JsonItemExporter, CsvItemExporter
import redis
import pymongo
import json

# 1.数据源管道
class AqiDataPipeline(object):
    def process_item(self, item, spider):
        # 抓取时间
        item['crawl_time'] = datetime.utcnow()
        # 那个爬虫
        item['spider'] = spider.name
        print(item)
        return item


# 2.json管道
class AqiJsonPipeline(object):
    def open_spider(self, spider):
        self.file = open('aqi.json', 'wb')
        self.writer = JsonItemExporter(self.file)
        self.writer.start_exporting()

    def process_item(self, item, spider):
        # 抓取时间
        # item['crawl_time'] = datetime.utcnow()
        # # 那个爬虫
        # item['spider'] = spider.name
        self.writer.export_item(item)
        return item

    def close_spider(self, spider):
        self.writer.finish_exporting()
        self.file.close()


# 3.csv管道
class AqiCsvPipeline(object):
    def open_spider(self, spider):
        self.file = open('aqi.csv', 'wb')
        self.writer = CsvItemExporter(self.file)
        self.writer.start_exporting()

    def process_item(self, item, spider):
        # 抓取时间
        # item['crawl_time'] = datetime.utcnow()
        # # 那个爬虫
        # item['spider'] = spider.name
        self.writer.export_item(item)
        return item

    def close_spider(self, spider):
        self.writer.finish_exporting()
        self.file.close()


# 4.readis管道
class AqiReadisPipeline(object):
    def open_spider(self, spider):
        # 链接数据库
        self.client = redis.StrictRedis(host='127.0.0.1', port=6379)
        # 存储key
        self.save_key = 'aqi_redis'

    def process_item(self, item, spider):
        # 抓取时间
        # item['crawl_time'] = datetime.utcnow()
        # # 那个爬虫
        # item['spider'] = spider.name
        # self.client.lpush(self.save_key, "{'abc': '123'}")
        # print("*"*100)
        # print(type(item))
        self.client.lpush(self.save_key, json.dumps(dict(item)))
        return item


# 5.mongodb管道
class AqiMongodbPipeline(object):
    def open_spider(self, spider):
        # 链接数据库
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        # 数据库名字和集合名字
        self.collection = self.client.AQI.aqi

    def process_item(self, item, spider):
        # 抓取时间
        # item['crawl_time'] = datetime.utcnow()
        # # 那个爬虫
        # item['spider'] = spider.name
        self.collection.insert(item)
        return item
