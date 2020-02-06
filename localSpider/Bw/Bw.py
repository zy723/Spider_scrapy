#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@contact: zy723@vip.qq.com
@site: 
@software: PyCharm
@file: Bw.py
@time: 2020/2/5 11:00
"""
import requests
import hashlib
import time
import json


class AppToken(object):
    """
    手机令牌生成
    """

    def __init__(self):
        pass

    def get_token(self, user_id):
        """
        手机令牌生成
        2018-05-31 00:26 + user_id
        :param user_id:用户Id  eg:148700
        :return:6位验证码
        """
        enc_str = time.strftime('%Y-%m-%d %H:%M') + user_id
        hash_256_str = hashlib.sha256(enc_str.encode()).hexdigest()
        short_array = hash_256_str[-12::]
        token_code = ''
        for i in range(6):
            temp_char = short_array[i * 2:i * 2 + 2]
            hex_num = int(temp_char, 16)
            hex_num_str = str(hex_num)
            if len(token_code) == 5:
                token_code = token_code + hex_num_str[:1:]
            elif len(token_code) == 4:
                if hex_num < 10:
                    token_code = token_code + hex_num_str[:1:]
                else:
                    token_code = (token_code + hex_num_str[:1:]) + hex_num_str[1:2:]
            elif len(token_code) >= 6:
                break
            else:
                token_code = token_code + hex_num_str
        return token_code


class BaoWuVpn(object):
    """
    VPN 登陆类
    """

    def __init__(self):
        self.host = 'https://vpn1.baosteel.com/prx/000/'
        self.sessions = requests.session()
        self.sessions.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        }
        self.sessions.verify = False
        self.app_token = AppToken()

    def login_by_app_token(self, user_name, pass_word):
        # https://vpn1.baosteel.com/prx/000/http/localhost/login
        url = self.host + 'http/localhost/login'
        data = {
            'method': 'test',
            'uname': user_name,
            'pwd': pass_word,
            'authCode': self.app_token.get_token(user_name),
        }
        ret_txt = self.sessions.post(url, data=data).content.decode()
        print(ret_txt)
        if '您已成功登录' in ret_txt:
            self.write_local()
            return True
        else:
            return False

    def write_local(self):
        with open("cooike.txt", 'w', encoding='utf-8') as f:
            f.write(json.dumps(requests.utils.dict_from_cookiejar(self.sessions.cookies)))

    def form_local_input_session(self):
        _cookie = ''
        with open("cooike.txt", 'r', encoding='utf-8') as f:
            _cookie = f.read()
        return requests.utils.cookiejar_from_dict(json.loads(_cookie))

    def init(self):
        self.sessions.get('https://vpn1.baosteel.com/prx/000/https/bca.baogang.info/buap/vpnmessagePhone.html').content.decode()

    def get_image_code(self):
        """
        手机验证码登陆
        :return:
        """
        url = 'https://vpn2.baosteel.com/prx/000/https/bca.baogang.info/buap/restservice/vpnLogin/getImage'
        img = self.sessions.get(url, verify=False).content
        pass

    def login(self, user_name, pass_word):
        pass

    def run(self):
        self.init()
        self.login_by_app_token('', '')


class EHr(object):
    def __init__(self):
        self.vpn = BaoWuVpn()
        self.host = 'https://vpn1.baosteel.com/prx/000/'
        self.sessions = requests.session()
        self.sessions.headers = {
            'Host': 'vpn1.baosteel.com',
            'Connection': 'keep-alive',
            'Origin': 'https://vpn1.baosteel.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'nested-navigate',
            'Referer': 'https://vpn1.baosteel.com/prx/000/https/cas.baogang.info/cas/login?loginType=mixLogin&userSystem=ehr&cssName=bsts&redirectUrl=http://ehr.baogang.info/hs/index.jsp',
        }
        self.sessions.verify = False
        self.sessions.cookies = self.vpn.form_local_input_session()
        self.sessions.get('https://vpn1.baosteel.com/prx/000/http/ehr.baogang.info/hs/')

    def ehr_login(self, user_name, pass_word):
        # https://vpn1.baosteel.com/prx/000/https/cas.baogang.info/cas/login?loginType=mixLogin&userSystem=ehr&cssName=bsts&redirectUrl=http://ehr.baogang.info/hs/index.jsp
        # https://vpn1.baosteel.com/prx/000/
        url = self.host + 'https/cas.baogang.info/cas/login?loginType=mixLogin&userSystem=ehr&cssName=bsts&redirectUrl=http://ehr.baogang.info/hs/index.jsp'
        data = {
            'username': user_name,
            'password': pass_word,
            'useCert': 'false',
            'lt': '',
            'execution': 'e1s2',
            '_eventId': 'submit',
        }
        ret_text = self.sessions.post(url, data=data).content.decode()
        print(ret_text)

    def run2(self):
        self.ehr_login('', '')





if __name__ == "__main__":
    # func()
    # print(AppToken().get_token('140700'))
    BaoWuVpn().run()
    # EHr().run2()
