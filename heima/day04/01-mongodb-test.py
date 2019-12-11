# -*- coding: UTF-8 -*-

import pymongo
import json


def create_table():
    """
    创建 查询数据库
    :return:
    """
    # 1. 链接数据库
    client = pymongo.MongoClient(host='127.0.0.1', port=27017)

    # 2. 创建库
    db = client['pystu']

    # 3. 建表
    collection = db['python']

    # 4. 往数据库中插入json文件
    data_list = json.load(open('stu.json', 'r'))
    print(data_list)
    collection.insert(data_list)

    # 5. 关闭数据库
    client.close()


if __name__ == '__main__':
    create_table()
