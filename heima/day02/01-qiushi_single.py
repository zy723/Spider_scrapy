import requests
from xml import etree
import json

"""
  高类聚, 低耦合

"""

class QiushiSpider(object):
    def __init__(self):
        self.base_url = 'https://www.qiushibaike.com/hot/page/{}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }

    def get_url_list(self):
        """
        获取所有Url链接
        :return:

        """
        url_list = []
        for i in range(1, 2):
            url = self.base_url.format(i)
            url_list.append(url)
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

    def run(self):
        # 1. 获取所有链接地址
        url_list = self.get_url_list()
        # 发送请求
        for url in url_list:
            data = self.send_request(url)
            # 解析数据
            name_list = self.analysis_data(data)
            print(name_list)


if __name__ == '__main__':
    QiushiSpider().run()
