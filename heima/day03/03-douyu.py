import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup


class DouyuSpider(object):
    def __init__(self):
        self.base_url = "https://www.douyu.com/directory/all"
        self.driver = webdriver.Chrome()
        self.count = 0

    def parse_data(self, data):
        # 转换类型
        soup = BeautifulSoup(data, 'lxml')
        data_list = []
        # 房间名字
        room_name_list = soup.select('.DyListCover-content .DyListCover-intro')
        # 昵称
        room_nick_list = soup.select('.DyListCover-content .DyListCover-user')
        # 人气
        room_hot_list = soup.select('.DyListCover-content .DyListCover-hot')
        # 获取房间类型
        room_type_list = soup.select('.DyListCover-content .DyListCover-zone')

        for room_name, room_type, room_nick, room_hot in zip(room_name_list, room_type_list, room_nick_list,
                                                             room_hot_list):
            item = {}

            item['room_name'] = room_name.get_text().strip()
            item['room_type'] = room_type.get_text().strip()
            item['room_nick'] = room_nick.get_text().strip()
            item['room_hot'] = room_hot.get_text().strip()
            data_list.append(item)
            self.count += 1

        return data_list

    def loop_get_data(self):
        # 获取数据
        data = self.driver.page_source
        # print(data)
        data_list = []

        while True:
            if data.find('dy-Pagination-disabled dy-Pagination-next') != -1:
                break
            self.driver.find_element_by_class_name(' dy-Pagination-next').click()
            # 解析数据
            data_list.append(self.parse_data(data))

        return data_list


    def run(self):
        self.driver.get(self.base_url)

        data_list = self.loop_get_data()



        # time.sleep(3)
        # 关闭浏览器
        self.driver.quit()

        print(data_list)

        print('总共的房间:{}'.format(self.count))


if __name__ == '__main__':
    DouyuSpider().run()
