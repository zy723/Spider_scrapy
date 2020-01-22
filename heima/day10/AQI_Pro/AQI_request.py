import pyDes
from Crypto.Cipher import AES
import hashlib, json, time, base64, requests
from lxml import etree
import execjs
import re

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


class AQIData(object):
    def __init__(self):
        self.base_host = 'https://www.aqistudy.cn'

    def get_history_data(self, city, month):
        """

        const askU7Pz0hYVb = "aQbRsUypdLd2eNSZ";
        const asioCAlPARXJ = "bkO067xmKeXSXHG4";
        const ackk2AuIYKun = "dvCs3EjGhB1KFDi4";
        const aciEYA1rAGZk = "fN65hQVLn4GTWfA7";
        const dskMriSZe7l3 = "hYhPB7zF8gv2HeAo";
        const dsiC0DdtBoEE = "xbFyhKq5UP9DT3Wl";
        const dckA1XHI6K0M = "oIAU0nA6P9T2XxpU";
        const dciSg16lXe2n = "pPnpt3QH2V2LZxjt";
        const aes_local_key = 'emhlbnFpcGFsbWtleQ==';
        const aes_local_iv = 'emhlbnFpcGFsbWl2';

        const askOBMGmB75S = "aPqPQcf1Ine2f4QB";
        const asiDO6lJkWm0 = "bwJrQdFDfsaCCGd2";
        const ackWgp0jYMZI = "d56AdlQNlsO5Cx9g";
        const aciAZZEXJJoB = "f8fZViDZEFI14sZi";
        const dskmTMSx0xca = "hFa3eEXyBmwuGM2H";
        const dsi0Ja0YkzkD = "xSB40RttS8jjqwRq";
        const dckdYKmHRXow = "oCzXViHAa3Ze3NrF";
        const dciAtAs475r5 = "px5gjnKXZFAJxcCL";
        const aes_local_key = 'emhlbnFpcGFsbWtleQ==';
        const aes_local_iv = 'emhlbnFpcGFsbWl2';


        function dNts5M8favlljUkeI(data) {
        data = BASE64.decrypt(data);
        data = DES.decrypt(data, dskMriSZe7l3, dsiC0DdtBoEE);
        data = AES.decrypt(data, askU7Pz0hYVb, asioCAlPARXJ);
        data = BASE64.decrypt(data);
        return data
        }
        e3e6b23f26ade009cdb97eb741c1c11e

        appId = '7a4ebffe96d76a8fc26c6373797f01e2';
        var clienttype = 'WEB';
        var timestamp = new Date().getTime();
        var param = {
            appId: appId,
            method: method,
            timestamp: timestamp,
            clienttype: clienttype,
            object: obj,
            secret: hex_md5(appId + method + timestamp + clienttype + JSON.stringify(ObjectSort(obj)))
        };
        param = BASE64.encrypt(JSON.stringify(param));

        :param city:
        :param month:
        :return:
        """
        url = self.base_host + '/historydata/api/historyapi.php'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.aqistudy.cn/historydata/daydata.php?city=%E6%8A%9A%E9%A1%BA&month=2019-11',
            'Accept-Language': 'zh-CN',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
            'Host': 'www.aqistudy.cn',
            'Content-Length': '282',
            'Connection': 'Keep-Alive',
            'Cache-Control': 'no-cache',
        }

        # {"appId":"cad7ce0505844254702142820e4a5b1e","method":"GETDAYDATA","timestamp":1579656267581,"clienttype":"WEB","object":{"city":"抚顺","month":"201911"},"secret":"bbff43b4faae28b1010337bf5d6d02fa"}
        appId = '7a4ebffe96d76a8fc26c6373797f01e2'
        method = 'GETDAYDATA'
        # timestamp = int(time.time() * 1000)
        timestamp = 1579659753530
        clienttype = 'WEB'
        obj = {"city": city, "month": month}
        # 7a4ebffe96d76a8fc26c6373797f01e2GETDAYDATA1579659753530WEB{"city":"抚顺","month":"201911"}
        # a7d45c881ac916b680a6477c04c9fbe6
        secret = hashlib.md5((appId + method + str(timestamp) + clienttype + json.dumps(obj).encode('utf-8').decode(
            'unicode_escape').replace(': ', ':').replace(', ', ',')).encode()).hexdigest()
        base_data = {"appId": appId,
                     "method": method,
                     "timestamp": timestamp,
                     "clienttype": clienttype,
                     "object": obj,
                     "secret": secret
                     }
        param = base64.b64encode(
            json.dumps(base_data).encode('utf-8').decode('unicode_escape').replace(': ', ':').replace(', ',
                                                                                                      ',').encode()).decode()
        data = {
            'h3TVqn5AG': param
        }
        tt = requests.post(url, data=data, headers=headers).content.decode()
        print(tt)

    def get_enc_key(self):
        url = 'https://www.aqistudy.cn/historydata/daydata.php?city=%E6%8A%9A%E9%A1%BA&month=2019-11'
        ret = requests.get(url).content.decode()
        html = etree.HTML(ret)
        path = html.xpath('//script[2]/@src')[0]
        enc_url = self.base_host + '/historydata/' + path
        # print(enc_url)
        ret_tt = requests.get(enc_url).content.decode().replace('eval', '')
        ret_t = execjs.eval(ret_tt).replace('const', 'var')
        print(ret_t)

        ret_t1 = re.findall('var .*?="(.*?)";', ret_t)
        ret_t2 = re.findall("appId='(.*?)'", ret_t)


        print(ret_t1)
        print(ret_t2)
    def re_test(self, ss):
        str = '''const askvAIqYSPfc="a90ABfGa7SptZkJb";const asiLMjsqRWcr="bExihGISzPax52jB";const ackBhgi4WCcC="d92Sp2tQD02zFklG";const aciYs9AKeRLP="fNx4lGT9vgbNb7rp";const dskYHwhoMeyb="hA3DoZ3cAaga7aHH";const dsiHkqM8wTSz="xGVIn6dPjHifhsFB";const dckpvOAYk1VH="o47ZyLL6BCGNaTY6";const dcikfZ55tR7h="plOAK5GtS2599BcY";const aes_local_key='emhlbnFpcGFsbWtleQ==';const aes_local_iv='emhlbnFpcGFsbWl2';var BASE64={encrypt:function(text){var b=new Base64();return b.encode(text)},decrypt:function(text){var b=new Base64();return b.decode(text)}};var DES={encrypt:function(text,key,iv){var secretkey=(CryptoJS.MD5(key).toString()).substr(0,16);var secretiv=(CryptoJS.MD5(iv).toString()).substr(24,8);secretkey=CryptoJS.enc.Utf8.parse(secretkey);secretiv=CryptoJS.enc.Utf8.parse(secretiv);var result=CryptoJS.DES.encrypt(text,secretkey,{iv:secretiv,mode:CryptoJS.mode.CBC,padding:CryptoJS.pad.Pkcs7});return result.toString()},decrypt:function(text,key,iv){var secretkey=(CryptoJS.MD5(key).toString()).substr(0,16);var secretiv=(CryptoJS.MD5(iv).toString()).substr(24,8);secretkey=CryptoJS.enc.Utf8.parse(secretkey);secretiv=CryptoJS.enc.Utf8.parse(secretiv);var result=CryptoJS.DES.decrypt(text,secretkey,{iv:secretiv,mode:CryptoJS.mode.CBC,padding:CryptoJS.pad.Pkcs7});return result.toString(CryptoJS.enc.Utf8)}};var AES={encrypt:function(text,key,iv){var secretkey=(CryptoJS.MD5(key).toString()).substr(16,16);var secretiv=(CryptoJS.MD5(iv).toString()).substr(0,16);secretkey=CryptoJS.enc.Utf8.parse(secretkey);secretiv=CryptoJS.enc.Utf8.parse(secretiv);var result=CryptoJS.AES.encrypt(text,secretkey,{iv:secretiv,mode:CryptoJS.mode.CBC,padding:CryptoJS.pad.Pkcs7});return result.toString()},decrypt:function(text,key,iv){var secretkey=(CryptoJS.MD5(key).toString()).substr(16,16);var secretiv=(CryptoJS.MD5(iv).toString()).substr(0,16);secretkey=CryptoJS.enc.Utf8.parse(secretkey);secretiv=CryptoJS.enc.Utf8.parse(secretiv);var result=CryptoJS.AES.decrypt(text,secretkey,{iv:secretiv,mode:CryptoJS.mode.CBC,padding:CryptoJS.pad.Pkcs7});return result.toString(CryptoJS.enc.Utf8)}};var localStorageUtil={save:function(name,value){var text=JSON.stringify(value);text=BASE64.encrypt(text);text=AES.encrypt(text,aes_local_key,aes_local_iv);try{localStorage.setItem(name,text)}catch(oException){if(oException.name==='QuotaExceededError'){console.log('超出本地存储限额！');localStorage.clear();localStorage.setItem(name,text)}}},check:function(name){return localStorage.getItem(name)},getValue:function(name){var text=localStorage.getItem(name);var result=null;if(text){text=AES.decrypt(text,aes_local_key,aes_local_iv);text=BASE64.decrypt(text);result=JSON.parse(text)}return result},remove:function(name){localStorage.removeItem(name)}};function getDataFromLocalStorage(key,period){if(typeof period==='undefined'){period=0}var d=DES.encrypt(key);d=BASE64.encrypt(key);var data=localStorageUtil.getValue(key);if(data){const time=data.time;const current=new Date().getTime();if(new Date().getHours()>=0&&new Date().getHours()<5&&period>1){period=1}if(current-(period*60*60*1000)>time){data=null}if(new Date().getHours()>=5&&new Date(time).getDate()!==new Date().getDate()&&period===24){data=null}}return data}function ObjectSort(obj){var newObject={};Object.keys(obj).sort().map(function(key){newObject[key]=obj[key]});return newObject}function d8l2PXTRWQKU1(data){data=BASE64.decrypt(data);data=DES.decrypt(data,dskYHwhoMeyb,dsiHkqM8wTSz);data=AES.decrypt(data,askvAIqYSPfc,asiLMjsqRWcr);data=BASE64.decrypt(data);return data}var p7XD6tBQIa9UNqq=(function(){function ObjectSort(obj){var newObject={};Object.keys(obj).sort().map(function(key){newObject[key]=obj[key]});return newObject}return function(method,obj){var appId='54ed6b8519e8aed1c76f2d948941258e';var clienttype='WEB';var timestamp=new Date().getTime();var param={appId:appId,method:method,timestamp:timestamp,clienttype:clienttype,object:obj,secret:hex_md5(appId+method+timestamp+clienttype+JSON.stringify(ObjectSort(obj)))};param=BASE64.encrypt(JSON.stringify(param));param=DES.encrypt(param,dckpvOAYk1VH,dcikfZ55tR7h);return param}})();function skSctZXWtfL88(method,object,callback,period){const key=hex_md5(method+JSON.stringify(object));const data=getDataFromLocalStorage(key,period);if(!data){var param=p7XD6tBQIa9UNqq(method,object);$.ajax({url:'api/historyapi.php',data:{h9159K32Z:param},type:"post",success:function(data){data=d8l2PXTRWQKU1(data);obj=JSON.parse(data);if(obj.success){if(period>0){obj.result.time=new Date().getTime();localStorageUtil.save(key,obj.result)}callback(obj.result)}else{console.log(obj.errcode,obj.errmsg)}}})}else{callback(data)}}'''
        ret_t = re.findall('var .*?="(.*?)";', str)
        ret_t2 = re.findall("appId='(.*?)'", str)


        print(ret_t)
        print(ret_t2)


    def run(self):
        # self.get_history_data("抚顺", "201911")
        self.get_enc_key()
        # self.re_test()


if __name__ == '__main__':
    # 三种查询方式
    # get_aqistudy('GETDETAIL', '上海', 'HOUR', '2018-11-06 05:00:00', '2018-11-06 08:00:00')
    # get_aqistudy('GETCITYWEATHER', '上海', 'HOUR', '2018-11-06 05:00:00', '2018-11-06 08:00:00')
    # get_history('上海', '201811')

    # get_test()

    AQIData().run()
