import requests
from xml import etree
import json
from queue import Queue
import threading

"""
  高类聚, 低耦合

"""


class QiushiSpider(object):
    def __init__(self):
        self.base_url = 'https://www.qiushibaike.com/hot/page/{}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }

        self.url_queue = Queue()
        self.response_queue = Queue()
        self.data_queue = Queue()

    def get_url_list(self):
        """
        获取所有Url链接
        :return:

        """
        # url_list = []
        for i in range(1, 2):
            url = self.base_url.format(i)
            # url_list.append(url)
            # url 地址入栈
            self.url_queue.put(url)
        # return url_list

    def send_request(self):
        """
        发送请求
        :return:
        """
        while True:
            url = self.url_queue.get()

            reponse = requests.get(url, headers=self.headers)
            data = reponse.content
            # 响应对象入栈
            self.response_queue.put(data)
            # return data

            # 计数器减一
            self.url_queue.task_done()

    def analysis_data(self):
        """
        解析数据
        :return:
        """
        while True:
            data = self.data_queue.get()

            html_data = etree.HTML(data)
            # 获取帖子数量
            div_list = html_data.xpath('//div[@id="content-left"]/div')

            name_list = []
            # 遍历出每页中存在的帖子数
            for div in div_list:
                nick_name = div.xpath('.//h2/text()')[0]
                print(nick_name.strip())
                name_list.append(nick_name.strip())
            # return name_list
            # 数据入栈
            self.data_queue.put(name_list)

            self.data_queue.task_done()

    def write_file(self):
        """
        保存数据到本地
        :return:
        """
        while True:
            data = self.data_queue.get()

            with open('qiushibaike.html', 'wb') as f:
                f.write(data)
            self.data_queue.task_done()

    def _start(self):
        # 1. 获取所有链接地址
        self.get_url_list()
        # 发送请求
        self.send_request()

        self.analysis_data()
        self.write_file()

    def run(self):
        self._start()


if __name__ == '__main__':
    QiushiSpider().run()
