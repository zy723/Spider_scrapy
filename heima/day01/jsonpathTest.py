import jsonpath
import requests
import json

if __name__ == '__main__':
    # 1.json_url
    json_url = 'https://www.lagou.com/lbs/getAllCitySearchLabels.json'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

    # 发送请求
    response = requests.get(json_url, headers=headers)
    data = response.content
    data_str = data.decode('utf-8')
    data_dict = json.loads(data_str)

    # 解析 jsonpath
    result_list = jsonpath.jsonpath(data_dict, '$..name')

    # 写出文件
    # print(result_list)

    json.dump(result_list, open('02.city.json', 'w'))
