import pyDes
from Crypto.Cipher import AES
import hashlib, json, time, base64, requests


class DES(object):
    # IV必须是 8 字节长度的十六进制数
    # key加密密钥长度，24字节

    def __init__(self, iv, key):
        self.iv = iv  # 偏移量
        self.key = key  # 密钥

    def encrypt(self, data):
        k = pyDes.des(self.key, pyDes.CBC, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)  # DES
        d = k.encrypt(data)
        d = base64.encodestring(d)
        return d

    def decrypt(self, data):
        k = pyDes.des(self.key, pyDes.CBC, self.iv, pad=None, padmode=pyDes.PAD_PKCS5)
        data = base64.decodestring(data)
        d = k.decrypt(data)
        return d


def DES_decrypt(decrypted_text):
    '''DES解密'''
    encryptdata = decrypted_text.encode()
    des = DES('9ff4453b', '863f30c7f96c96fb')
    decryptdata = des.decrypt(encryptdata)
    return decryptdata


def DES_decrypt_history(decrypted_text):
    '''DES解密(history接口)'''
    encryptdata = decrypted_text.encode()
    des = DES('xESOOshClMDMuOuE', 'higQZAEabUbp4G0K')  # iv,key
    decryptdata = des.decrypt(encryptdata)
    return decryptdata


BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def add_to_16(text):
    # str不是16的倍数那就补足为16的倍数
    while len(text) % 16 != 0:
        text += '\0'
    return str.encode(text)  # 返回bytes


def pkcs7padding(data):
    bs = AES.block_size
    padding = bs - len(data) % bs
    padding_text = chr(padding) * padding
    return data + padding_text


def AES_encrypt(text):
    '''AES加密'''
    # text:待加密文本
    text = pkcs7padding(text)
    key = 'd0936268a554ed2a'  # 密钥key
    iv = b'2441e23aca5285a8'  # 偏移量IV
    aes = AES.new(add_to_16(key), AES.MODE_CBC, iv)  # 初始化加密器
    encrypted_text = str(base64.encodebytes(aes.encrypt(add_to_16(text))), encoding='utf8').replace('\n', '')  # 加密
    # print('AES加密值:', encrypted_text)
    return encrypted_text


def AES_decrypt(encrypted_text):
    '''AES解密'''
    # text:待解密文本
    encrypted_text = pkcs7padding(encrypted_text)
    key = '6faf4a2fa46ac1cb'  # 密钥key
    iv = b'4d6c56abc669f198'  # 偏移量IV
    aes = AES.new(add_to_16(key), AES.MODE_CBC, iv)  # 初始化加密器
    decrypted_text = str(
        aes.decrypt(base64.decodebytes(bytes(encrypted_text, encoding='utf8'))).rstrip(b'\0').decode("utf8"))  # 解密
    # print('解密值：', decrypted_text)
    return decrypted_text


def AES_encrypt_history(text):
    '''AES加密(history接口)'''
    # text:待加密文本
    text = pkcs7padding(text)
    key = 'd9sF1BBD3ICeDVGg'  # 密钥key
    iv = b'fCvq8j6xDqmNcDvu'  # 偏移量IV
    aes = AES.new(add_to_16(key), AES.MODE_CBC, iv)  # 初始化加密器
    encrypted_text = str(base64.encodebytes(aes.encrypt(add_to_16(text))), encoding='utf8').replace('\n', '')  # 加密
    # print('AES加密值:', encrypted_text)
    return encrypted_text


def AES_decrypt_history(encrypted_text):
    '''AES解密(history接口)'''
    # text:待解密文本
    encrypted_text = pkcs7padding(encrypted_text)
    key = 'aGE84jwkIFOkOQfK'  # 密钥key
    iv = b'bU2VU2tSPNNAQPbM'  # 偏移量IV
    aes = AES.new(add_to_16(key), AES.MODE_CBC, iv)  # 初始化加密器
    decrypted_text = str(
        aes.decrypt(base64.decodebytes(bytes(encrypted_text, encoding='utf8'))).rstrip(b'\0').decode("utf8"))  # 解密
    # print('解密值：', decrypted_text)
    return decrypted_text


# 天气数据详细网址: https://www.aqistudy.cn/html/city_detail.html
def get_aqistudy(method, city, type, startTime, endTime):
    '''
    按小时/日/月查询
    :param method: 查询数据方法 (1."GETDETAIL"-详情数据:time,aqi,pm2_5,pm10,co,no2,o3,so2,rank;2."GETCITYWEATHER"-天气数据:time,temp,humi,wse,wd,tq)
    :param city: 查询城市 (eg:"北京")
    :param type: 查询时间类型三种(时HOUR/日DAY/月MONTH)
    :param startTime: 起始时间 (eg:"2018-11-03 10:00:00")
    :param endTime: 结束时间 (eg:"2018-11-03 13:00:00")
    :returns weather_data: 天气数据
    '''

    # Step1:加密提交参数
    queryparam = {
        'city': city,  # 城市
        'endTime': endTime,  # 结束时间
        'startTime': startTime,  # 起始时间
        'type': type  # 查询时间类型3种: 时(HOUR)/日(DAY)/月(MONTH)
    }
    appId = '1a45f75b824b2dc628d5955356b5ef18'
    clienttype = 'WEB'
    timestamp = str(int(time.time() * 1000))
    json_2 = json.dumps(queryparam).encode('utf-8').decode('unicode_escape').replace(': ', ':').replace(', ', ',')
    param = {
        'appId': appId,
        'method': method,
        'timestamp': int(timestamp),
        'clienttype': clienttype,
        'object': queryparam,
        'secret': hashlib.md5((appId + method + timestamp + clienttype + json_2).encode()).hexdigest()
    }
    json_3 = json.dumps(param).encode('utf-8').decode('unicode_escape').replace(': ', ':').replace(', ', ',').encode()
    param = base64.b64encode(json_3).decode()
    aes_encrypted = AES_encrypt(param)
    url = 'https://www.aqistudy.cn/apinew/aqistudyapi.php'
    data = {'d': aes_encrypted}
    headers = {
        'Host': 'www.aqistudy.cn',
        'Origin': 'https://www.aqistudy.cn',
        'Referer': 'https://www.aqistudy.cn/html/city_detail.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    html = requests.post(url, data=data, headers=headers)
    encrypted_data = html.text

    # Step2:解密返回的加密数据
    '''
    解密函数:
    function decodeData(data) {
    data = AES.decrypt(data, aes_server_key, aes_server_iv);
    data = DES.decrypt(data, des_key, des_iv);
    data = BASE64.decrypt(data);
    return data
    }
    '''
    aes_decrypted = AES_decrypt(encrypted_data)
    des_decrypted = DES_decrypt(aes_decrypted)
    weather_data = base64.b64decode(des_decrypted).decode()
    print(weather_data)
    # Step3:解析天气数据
    data = json.loads(weather_data)
    if data.get('success') == True and data.get('errcode') == 0:
        print('恭喜您,查询天气数据成功!')
        data = data.get('result').get('data')
        total = data.get('total')
        print('一共查询到{}组数据:'.format(total))
        for i in data.get('rows'):
            print(i)
    else:
        print('抱歉,查询天气数据失败!请核对查询参数是否正确!')


# 历史数据查询网址: https://www.aqistudy.cn/historydata/monthdata.php?city=%E5%8C%97%E4%BA%AC
def get_history(city, month):
    '''
    按月查询每天的历史数据
    :param city: 查询城市 (eg:"北京")
    :param month: 查询月份(eg:"201811"; 即查询2018年11月每天的数据)
    :returns weather_data: 天气数据
    '''

    # Step1:加密提交参数
    # 查询数据方法
    method = "GETDAYDATA"
    queryparam = {
        'city': city,  # 城市 eg: "北京"
        'month': month  # 只能按月查询 eg: "201811"
    }
    # (1)Base64加密
    appId = 'ba0c300c64f8685b828df375629af09f'
    clienttype = 'WEB'
    timestamp = str(int(time.time() * 1000))
    json_2 = json.dumps(queryparam).encode('utf-8').decode('unicode_escape').replace(': ', ':').replace(', ', ',')
    param = {
        'appId': appId,
        'method': method,
        'timestamp': int(timestamp),
        'clienttype': clienttype,
        'object': queryparam,
        'secret': hashlib.md5((appId + method + timestamp + clienttype + json_2).encode()).hexdigest()
    }
    json_3 = json.dumps(param).encode('utf-8').decode('unicode_escape').replace(': ', ':').replace(', ', ',').encode()
    param = base64.b64encode(json_3).decode()
    aes_encrypted = AES_encrypt_history(param)
    url = 'https://www.aqistudy.cn/historydata/api/historyapi.php'
    data = {'h1BEKEez0': aes_encrypted}
    headers = {
        'Host': 'www.aqistudy.cn',
        'Origin': 'https://www.aqistudy.cn',
        'Referer': 'https://www.aqistudy.cn/html/city_detail.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    html = requests.post(url, data=data, headers=headers)
    encrypted_data = html.text
    print('返回加密数据:' + encrypted_data)
    # Step2:解密返回的加密数据
    '''
    解密函数:
    function decodeData(data) {
    data = BASE64.decrypt(data);
    data = DES.decrypt(data, des_key, des_iv);
    data = AES.decrypt(data, aes_server_key, aes_server_iv);
    data = BASE64.decrypt(data);
    return data
    }
    '''
    base64_decrypted = base64.b64decode(encrypted_data).decode()
    des_decrypted = DES_decrypt_history(base64_decrypted).decode()
    aes_decrypted = AES_decrypt_history(des_decrypted)
    weather_data = base64.b64decode(aes_decrypted).decode()
    print(weather_data)
    # Step3:解析天气数据
    data = json.loads(weather_data)
    if data.get('success') == True and data.get('errcode') == 0:
        print('恭喜您,查询天气数据成功!')
        data = data.get('result').get('data')
        total = data.get('num')
        print('一共查询到{}组数据:'.format(total))
        for i in data.get('items'):
            print(i)
    else:
        print('抱歉,查询天气数据失败!请核对查询参数是否正确!')


def get_test():
    url = 'https://www.aqistudy.cn/historydata/'
    headers = {
        'Host': 'www.aqistudy.cn',
        'Origin': 'https://www.aqistudy.cn',
        'Referer': 'https://www.aqistudy.cn/html/city_detail.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    ret_txt = requests.get(url, headers=headers).content.decode()
    print(ret_txt)


if __name__ == '__main__':
    # 三种查询方式
    # get_aqistudy('GETDETAIL', '上海', 'HOUR', '2018-11-06 05:00:00', '2018-11-06 08:00:00')
    # get_aqistudy('GETCITYWEATHER', '上海', 'HOUR', '2018-11-06 05:00:00', '2018-11-06 08:00:00')
    # get_history('上海', '201811')

    get_test()
