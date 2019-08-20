# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import json
from urllib.parse import urljoin


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com', 'p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        # 获取大分类
        dt_list = response.xpath("//div[@class='mc']/dl/dt")

        for dt in dt_list:
            item = {}
            item['b_cate'] = dt.xpath("./a/text()").extract_first()
            # 小分类
            em_list = dt.xpath("following-sibling::dd[1]/em")

            for em in em_list:
                item['s_href'] = em.xpath("./a/@href").extract_first()
                item['s_cate'] = em.xpath("./a/text()").extract_first()
                if item['s_href'] is not None:
                    # item['s_href'] = 'https://' + item['s_href']
                    item['s_href'] = urljoin(response.url, item['s_href'])
                    yield scrapy.Request(
                        item['s_href'],
                        callback=self.parse_book_list,
                        meta={"item": deepcopy(item)}
                    )

    def parse_book_list(self, response):
        """
        解析列表页
        :param response:
        :return:
        """
        item = response.meta['item']
        li_list = response.xpath("//div[@id='plist']/ul/li")

        for li in li_list:
            item['book_img'] = li.xpath(".//div[@class='p-img']//img/@src").extract_first()
            if item['book_img'] is None:
                item['book_img'] = li.xpath(".//div[@class='p-img']//img/@data-lazy-img").extract_first()
            item['book_img'] = urljoin(response.url, item['book_img'])
            item['book_name'] = li.xpath(".//div[@class='p-name']/a/em/text()").extract_first().strip()  # 书名
            item['book_author'] = li.xpath(".//span[@class='author_type_1']/a/text()").extract()  # 作者
            item['book_press'] = li.xpath(".//span[@class='p-bi-store']/a/@title").extract_first()  # 出版社
            item['book_publish_date'] = li.xpath(".//span[@class='p-bi-date']/text()").extract_first().strip()  # 出版日期
            item["book_sku"] = li.xpath("./div/@data-sku").extract_first()  # 库存编号
            sku_url = 'https://p.3.cn/prices/mgets?skuIds={}'.format(item['book_sku'])

            yield scrapy.Request(
                sku_url,
                callback=self.parse_book_price,
                meta={'item': deepcopy(item)}
            )

            # 翻页
            next_url = response.xpath("//a[@class='pn-next']/@href").extract_first()
            if next_url is not None:
                next_url = urljoin(response.url, next_url)
                yield scrapy.Request(
                    next_url,
                    callback=self.parse_book_list,
                    meta={'item': item}
                )

    def parse_book_price(self, response):
        """
        解析价格
        :param response:
        :return:
        """
        item = response.meta['item']
        item['book_price'] = json.loads(response.body.decode())[0]['op']
        print(item)
