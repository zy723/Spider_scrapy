import requests
import re
import json


class NeiHanbaSpider(object):
    def __init__(self):
        self.base_url = ''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
        self.first_pasttern = re.compile('<div class="f18 mb12">(.*?)</div>', re.S)

    def send_request(self):
        try:
            response = requests.get(self.base_url, headers=self.headers)
            data = response.content.decode('gbk')
            return data
        except:
            print("no response")
            return None

    def parse_data(self, data):
        return_list = self.first_pasttern.findall(data)

        return return_list

    def write_file(self, data_list):
        with open('neihanba.html', 'w') as f:
            for content in data_list:
                f.write(content)

    def run(self):
        # 发送请求
        data = self.send_request()
        if data:
            # 解析数据
            data_list = self.parse_data(data)
            # 保存数据
            self.write_file(data_list)


if __name__ == '__main__':
    NeiHanbaSpider().run()
