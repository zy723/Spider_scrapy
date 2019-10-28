import pafy
from lxml import etree
import requests
import jsonpath
import json
import re
import os


class YoutubeVideoDownload(object):

    def __init__(self):
        # self.download_url = url  # 绑定到url
        self.host = 'https://www.youtube.com/'
        # self.startUrl = startUrl
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

    def get_down_url(self, ll_url):
        # 获取下载地址
        try:
            video = pafy.new(self.host + ll_url)
            v_best = video.getbest()  # 下载最清晰画质
            # print(v_best.title)
            return v_best.url, v_best.title.replace('/', '').replace('|', '') + '.mp4'
        except:
            print(ll_url)
            return None

    def get_file_list(self):
        url_link = 'https://www.youtube.com/channel/UCvYqaFp_9gf5SPmNsDcri3A/videos?app=desktop&pbj=1'
        wb_data = requests.get(url_link, headers=self.headers).text
        # print(wb_data)
        # html = etree.HTML(wb_data)
        # with open('1.html', 'w', encoding='utf-8') as f:
        #     f.write(wb_data)
        rr = re.search(r'window\["ytInitialData"\] = (.*);', wb_data)
        print(rr.group(1))
        ll = jsonpath.jsonpath(json.loads(rr.group(1)),
                               '$..gridVideoRenderer.navigationEndpoint.commandMetadata.webCommandMetadata.url')
        return ll

        # html_list = html.xpath('//*[@id="thumbnail"]/@href')
        # for tmp_url in html_list:
        #     print(tmp_url)

    def get_file_list2(self):
        """
        通过 xpath 获取地址：//*[@id="thumbnail"]/@href

        :return:
        """
        str_xpath = """
        /watch?v=dFkmUpdBe5A&list=PL-a_q7EH140IeBMECO2AXeRjEzGOpjdeO&index=2&t=0s
        /watch?v=Had9ngH2fZA&list=PL-a_q7EH140IeBMECO2AXeRjEzGOpjdeO&index=3&t=0s
        /watch?v=eyb7Gla-ePo&list=PL-a_q7EH140IeBMECO2AXeRjEzGOpjdeO&index=4&t=0s
        /watch?v=G95DCF-q6a4&list=PL-a_q7EH140IeBMECO2AXeRjEzGOpjdeO&index=5&t=0s
        /watch?v=iCQ8yKM89Ow&list=PL-a_q7EH140IeBMECO2AXeRjEzGOpjdeO&index=6&t=0s
        /watch?v=hjfNBEg6Ev0&list=PL-a_q7EH140IeBMECO2AXeRjEzGOpjdeO&index=7&t=0s
        /watch?v=025p7-Dfup8&list=PL-a_q7EH140IeBMECO2AXeRjEzGOpjdeO&index=8&t=0s
        /watch?v=8ruSjqIGHM8&list=PL-a_q7EH140IeBMECO2AXeRjEzGOpjdeO&index=9&t=0s
        /watch?v=wsEaU_T6F2I&list=PL-a_q7EH140IeBMECO2AXeRjEzGOpjdeO&index=10&t=0s
        /watch?v=X5riFG_RmaU&list=PL-a_q7EH140IeBMECO2AXeRjEzGOpjdeO&index=11&t=0s
        /watch?v=DIWOi0S1tcA&list=PL-a_q7EH140IeBMECO2AXeRjEzGOpjdeO&index=12&t=0s
        /watch?v=pYgVJtJap6k&list=PL-a_q7EH140IeBMECO2AXeRjEzGOpjdeO&index=13&t=0s
        """
        tmp_list = re.findall(r'/.*\S', str_xpath)
        # print(tmp_list)
        return tmp_list

    def down_files(self, down_url, file_name, file_dir=r'F:\temp\UI_video\Fahim Tajwarul Islam'):
        # 使用本地Aria2下载
        url = 'http://127.0.0.1:6800/jsonrpc'
        download_url = down_url
        json_rpc = json.dumps({
            'id': '',
            'jsonrpc': '2.0',
            'method': 'aria2.addUri',
            'params': [[download_url],
                       {'dir': 'file_dir'.replace('file_dir', file_dir),
                        'out': 'file_name'.replace('file_name', file_name)}]
        })
        response = requests.post(url=url, data=json_rpc)
        print(response.text)

    def run(self):
        # 获取下载地址
        down_urls = self.get_file_list2()
        # print(len(down_urls))
        # 转换真正下载地址
        ii = 0
        for down_url in down_urls:
            ii += 1
            down_body = self.get_down_url(down_url)
            if down_body:
                print('正在下载第 ' + str(ii) + '/' + str(len(down_urls)) + ' 条视频')
                print(down_body[1])
                # 发送到本地下载地址
                self.down_files(down_body[0], down_body[1])


if __name__ == '__main__':
    YoutubeVideoDownload().run()
