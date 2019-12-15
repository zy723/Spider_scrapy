# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonItemExporter


class TencentPipeline(object):

    def open_spider(self, spider):
        self.file = open("tencent.json", 'wb')
        # 写入器
        self.writer = JsonItemExporter(self.file)
        self.writer.start_exporting()

    def process_item(self, item, spider):
        self.writer.export_item(item)
        return item

    def close_spider(self, spider):
        self.writer.finish_exporting()
        self.file.close()
