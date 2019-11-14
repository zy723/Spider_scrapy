import requests
import js2py
import jsonpath


class BaiduTransient(object):
    """
    百度翻译
    """

    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': 'BAIDUID=C552D093C28381486F24D9E2DD31BE46:FG=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1573666674; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; yjs_js_security_passport=af9205cfdc18da8f994c9273360d46e89198432e_1573666955_js; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1573666957; __yjsv5_shitong=1.0_7_130509a789ca2a9119ecf3f9c38d30f85b35_300_1573666962800_116.234.224.193_cd1ea4a1',
            'origin': 'https://fanyi.baidu.com',
            'referer': 'https://fanyi.baidu.com/?aldtype=16047'
        }

    def js_encode(self, str):
        js_code = """
        function a(r){if(Array.isArray(r)){for(var o=0,t=Array(r.length);o<r.length;o++)t[o]=r[o];return t}return Array.from(r)}function n(r,o){for(var t=0;t<o.length-2;t+=3){var a=o.charAt(t+2);a=a>="a"?a.charCodeAt(0)-87:Number(a),a="+"===o.charAt(t+1)?r>>>a:r<<a,r="+"===o.charAt(t)?r+a&4294967295:r^a}return r}function e(r){var o=r.match(/[\\uD800-\\uDBFF][\\uDC00-\\uDFFF]/g);if(null===o){var t=r.length;t>30&&(r=""+r.substr(0,10)+r.substr(Math.floor(t/2)-5,10)+r.substr(-10,10))}else{for(var e=r.split(/[\\uD800-\\uDBFF][\\uDC00-\\uDFFF]/),C=0,h=e.length,f=[];h>C;C++)""!==e[C]&&f.push.apply(f,a(e[C].split(""))),C!==h-1&&f.push(o[C]);var g=f.length;g>30&&(r=f.slice(0,10).join("")+f.slice(Math.floor(g/2)-5,Math.floor(g/2)+5).join("")+f.slice(-10).join(""))}var u=void 0,l=""+String.fromCharCode(103)+String.fromCharCode(116)+String.fromCharCode(107);var i;u="320305.131321201";for(var d=u.split("."),m=Number(d[0])||0,s=Number(d[1])||0,S=[],c=0,v=0;v<r.length;v++){var A=r.charCodeAt(v);128>A?S[c++]=A:(2048>A?S[c++]=A>>6|192:(55296===(64512&A)&&v+1<r.length&&56320===(64512&r.charCodeAt(v+1))?(A=65536+((1023&A)<<10)+(1023&r.charCodeAt(++v)),S[c++]=A>>18|240,S[c++]=A>>12&63|128):S[c++]=A>>12|224,S[c++]=A>>6&63|128),S[c++]=63&A|128)}for(var p=m,F=""+String.fromCharCode(43)+String.fromCharCode(45)+String.fromCharCode(97)+(""+String.fromCharCode(94)+String.fromCharCode(43)+String.fromCharCode(54)),D=""+String.fromCharCode(43)+String.fromCharCode(45)+String.fromCharCode(51)+(""+String.fromCharCode(94)+String.fromCharCode(43)+String.fromCharCode(98))+(""+String.fromCharCode(43)+String.fromCharCode(45)+String.fromCharCode(102)),b=0;b<S.length;b++)p+=S[b],p=n(p,F);return p=n(p,D),p^=s,0>p&&(p=(2147483647&p)+2147483648),p%=1e6,p.toString()+"."+(p^m)}function transientEnc(str){return e(str);}
        """
        context = js2py.EvalJs()
        context.execute(js_code)
        return context.transientEnc(str)

    def baidu_transient(self, str):
        tra_url = 'https://fanyi.baidu.com/v2transapi?from=zh&to=en'
        sign_en = self.js_encode(str)
        print(sign_en)
        body = {
            'from': 'zh',
            'to': 'en',
            'query': str,
            'transtype': 'realtime',
            'simple_means flag': 3,
            'sign': sign_en,
            'token': 'eeaa33fad36816adafa7e987ec56021c'
        }

        ret_str = self.session.post(tra_url, body).json()

        ret_tt = jsonpath.jsonpath(ret_str, '$..dst')

        print(ret_tt[0])

    def run(self):
        self.baidu_transient('不懂啊')


if __name__ == '__main__':
    BaiduTransient().run()
