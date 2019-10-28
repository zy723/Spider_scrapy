import requests
import json
import jsonpath
import time


class HrTenxun(object):
    def __init__(self):
        self.base_url = 'https://careers.tencent.com/tencentcareer/api/post/Query'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }

    def send_request(self, params):
        response = requests.get(self.base_url, headers=self.headers, params=params)

        return response.content.decode()

    def parse_data(self, data):
        json_str = json.loads(data)
        ret_list = jsonpath.jsonpath(json_str, '$..RecruitPostName')
        return ret_list

    def write_file(self):
        pass

    def run(self):
        page_index = 1

        params = {
            'timestamp': float(time.time()),
            'countryId': '',
            'cityId': '',
            'bgIds': '',
            'productId': '',
            'categoryId': '',
            'parentCategoryId': '',
            'attrId': '',
            'keyword': '',
            'pageIndex': page_index,
            'pageSize': '10',
            'language': 'zh-cn',
            'area': 'cn'
        }

        # 获取数据
        data = self.send_request(params)
        # 解析数据
        ret_list = self.parse_data(data)
        # 保存数据
        print(ret_list)


if __name__ == '__main__':
    HrTenxun().run()
