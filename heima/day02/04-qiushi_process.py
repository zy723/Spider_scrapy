import requests
from xml import etree
import json
import time
from queue import Queue
import threading
from multiprocessing import JoinableQueue
from multiprocessing import Process

"""
  高类聚, 低耦合
  
  多进程

"""


class QiushiSpider(object):
    def __init__(self):
        self.base_url = 'https://www.qiushibaike.com/hot/page/{}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }

        self.url_queue = JoinableQueue()
        self.response_queue = JoinableQueue()
        self.data_queue = JoinableQueue()

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

        # 1. 定义临时变量保存线程
        th_list = []
        # 2. 获取所有链接地址
        th_url = Process(target=self.get_url_list)
        th_list.append(th_url)

        # 3. 发送请求
        th_send = Process(target=self.send_request)
        th_list.append(th_send)

        # 4. 解析数据
        th_analysis = Process(target=self.analysis_data)
        th_list.append(th_analysis)

        # 5. 保存数据
        th_slave = Process(target=self.write_file)
        th_list.append(th_slave)

        # 6. 开启线程
        for th in th_list:
            # 保证 主线程结束, 子线程立即结束 (不会存在孤儿线程)
            th.daemon = True
            th.start()

        # 7. 用队列 阻塞主线程等待 子线程执行完毕
        for q in [self.url_queue, self.response_queue, self.data_queue]:
            q.join()

    def run(self):
        start_time = time.time()
        self._start()
        end_time = time.time()
        print('总耗时:{}'.format(end_time - start_time))


if __name__ == '__main__':
    QiushiSpider().run()
