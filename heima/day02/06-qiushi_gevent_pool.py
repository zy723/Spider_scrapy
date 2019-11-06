# 注意 gevent 导包 最上面
# socket 模块 阻塞改成非阻塞
from gevent.pool import Pool
import gevent.monkey

gevent.monkey.patch_all()

import requests
import time
from xml import etree

from queue import Queue

"""
  高类聚, 低耦合
  
  协成

"""


class QiushiSpider(object):
    def __init__(self):
        self.base_url = 'https://www.qiushibaike.com/hot/page/{}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }
        self.pool = Pool()
        self.url_queue = Queue()
        # 发送的数量
        self.request_number = 0
        # 已经完成数量
        self.response_number = 0
        self.is_running = True

    def get_url_list(self):
        """
        获取所有Url链接
        :return:

        """
        url_list = []
        for i in range(1, 2):
            url = self.base_url.format(i)
            url_list.append(url)
            self.url_queue.put(url)
        return url_list

    def send_request(self, url):
        """
        发送请求
        :return:
        """
        reponse = requests.get(url, headers=self.headers)
        data = reponse.content
        return data

    def analysis_data(self, data):
        """
        解析数据
        :return:
        """
        html_data = etree.HTML(data)
        # 获取帖子数量
        div_list = html_data.xpath('//div[@id="content-left"]/div')

        name_list = []
        # 遍历出每页中存在的帖子数
        for div in div_list:
            nick_name = div.xpath('.//h2/text()')[0]
            print(nick_name.strip())
            name_list.append(nick_name.strip())
        return name_list

    def write_file(self, data):
        """
        保存数据到本地
        :return:
        """
        with open('qiushibaike.html', 'wb') as f:
            f.write(data)

    def _start(self):
        # 获取url
        self.request_number += 1
        url = self.url_queue.get()
        data = self.send_request(url)
        content_data = self.analysis_data(data)
        self.write_file(content_data)
        self.url_queue.task_done()
        self.response_number += 1

    def _callback(self, temp):
        if self.is_running:
            self.pool.apply_async(self._start, callback=self._callback)

    def async_start(self):
        self.get_url_list()
        # 并发3次
        for ii in range(3):
            self.pool.apply_async(self._start, callback=self._callback)
        # 线程阻塞等待子线程完成
        while self.response_number < self.request_number:
            time.sleep(0.1)
        self.is_running = False

    def run(self):
        start_time = time.time()
        self.async_start()
        end_time = time.time()

        print('总花费时间:{}'.format(end_time - start_time))


if __name__ == '__main__':
    QiushiSpider().run()
