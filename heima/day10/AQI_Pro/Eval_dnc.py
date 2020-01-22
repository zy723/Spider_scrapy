#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@contact: zy723@vip.qq.com
@site: 
@software: PyCharm
@file: Eval_dnc.py
@time: 2020/1/22 14:52
"""
import re
import execjs

def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

def unpack(p, a, c, k, e=None, d=None):
    while (c):
        c-=1
        if (k[c]):
            p = re.sub("\\b" + baseN(c, a) + "\\b",  k[c], p)
    return p

encrypted = r'''eval(function(p,a,c,k,e,d){e=function(c){return c};if(!''.replace(/^/,String)){while(c--)d[c]=k[c]||c;k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1;};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p;}('5 11=17;5 12=["/3/2/1/0/13.4","/3/2/1/0/15.4","/3/2/1/0/14.4","/3/2/1/0/7.4","/3/2/1/0/6.4","/3/2/1/0/8.4","/3/2/1/0/10.4","/3/2/1/0/9.4","/3/2/1/0/23.4","/3/2/1/0/22.4","/3/2/1/0/24.4","/3/2/1/0/26.4","/3/2/1/0/25.4","/3/2/1/0/18.4","/3/2/1/0/16.4","/3/2/1/0/19.4","/3/2/1/0/21.4"];5 20=0;',10,27,'40769|54|Images|Files|png|var|imanhua_005_140430179|imanhua_004_140430179|imanhua_006_140430226|imanhua_008_140430242|imanhua_007_140430226|len|pic|imanhua_001_140429664|imanhua_003_140430117|imanhua_002_140430070|imanhua_015_140430414||imanhua_014_140430382|imanhua_016_140430414|sid|imanhua_017_140430429|imanhua_010_140430289|imanhua_009_140430242|imanhua_011_140430367|imanhua_013_140430382|imanhua_012_140430367'.split('|'),0,{}))'''
encrypted = r'''(function(p,a,c,k,e,d){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('g 1c="22";g 1n="1C";g 1k="1x";g 1a="1v";g 19="1u";g 18="1s";g 1G="1w";g 1F="1E";g S=\'1D==\';g R=\'1r\';2 z={l:9(4){2 b=r Y();h b.1t(4)},k:9(4){2 b=r Y();h b.1y(4)}};2 E={l:9(4,7,i){2 c=(3.u(7).j()).t(0,16);2 e=(3.u(i).j()).t(W,8);c=3.o.n.m(c);e=3.o.n.m(e);2 f=3.E.l(4,c,{i:e,w:3.w.L,M:3.H.O});h f.j()},k:9(4,7,i){2 c=(3.u(7).j()).t(0,16);2 e=(3.u(i).j()).t(W,8);c=3.o.n.m(c);e=3.o.n.m(e);2 f=3.E.k(4,c,{i:e,w:3.w.L,M:3.H.O});h f.j(3.o.n)}};2 A={l:9(4,7,i){2 c=(3.u(7).j()).t(16,16);2 e=(3.u(i).j()).t(0,16);c=3.o.n.m(c);e=3.o.n.m(e);2 f=3.A.l(4,c,{i:e,w:3.w.L,M:3.H.O});h f.j()},k:9(4,7,i){2 c=(3.u(7).j()).t(16,16);2 e=(3.u(i).j()).t(0,16);c=3.o.n.m(c);e=3.o.n.m(e);2 f=3.A.k(4,c,{i:e,w:3.w.L,M:3.H.O});h f.j(3.o.n)}};2 X={1d:9(s,17){2 4=B.N(17);4=z.l(4);4=A.l(4,S,R);1Y{C.10(s,4)}1X(14){q(14.s===\'1V\'){1e.1f(\'caochu\');C.1U();C.10(s,4)}}},1T:9(s){h C.15(s)},13:9(s){2 4=C.15(s);2 f=U;q(4){4=A.k(4,S,R);4=z.k(4);f=B.m(4)}h f},1R:9(s){C.1Q(s)}};9 1i(7,p){q(1O p===\'1N\'){p=0}2 d=E.l(7);d=z.l(7);2 6=X.13(7);q(6){g F=6.F;g 12=r x().V();q(r x().Q()>=0&&r x().Q()<5&&p>1){p=1}q(12-(p*11*11*1K)>F){6=U}q(r x().Q()>=5&&r x(F).Z()!==r x().Z()&&p===W){6=U}}h 6}9 T(a){2 D={};1o.1p(a).1m().1q(9(7){D[7]=a[7]});h D}9 1l(6){6=z.k(6);6=E.k(6,19,18);6=A.k(6,1c,1n);6=z.k(6);h 6}2 1g=(9(){9 T(a){2 D={};1o.1p(a).1m().1q(9(7){D[7]=a[7]});h D}h 9(y,a){2 I=\'1L\';2 G=\'1M\';2 J=r x().V();2 v={I:I,y:y,J:J,G:G,K:a,1P:1j(I+y+J+G+B.N(T(a)))};v=z.l(B.N(v));v=A.l(v,1k,1a);h v}})();9 1S(y,K,P,p){g 7=1j(y+B.N(K));g 6=1i(7,p);q(!6){2 v=1g(y,K);$.1W({1Z:\'1H/20.21\',6:{1J:v},1I:"1B",1b:9(6){6=1l(6);a=B.m(6);q(a.1b){q(p>0){a.f.F=r x().V();X.1d(7,a.f)}P(a.f)}1h{1e.1f(a.1A,a.1z)}}})}1h{P(6)}}',62,127,'||var|CryptoJS|text||data|key||function|obj||secretkey||secretiv|result|const|return|iv|toString|decrypt|encrypt|parse|Utf8|enc|period|if|new|name|substr|MD5|param|mode|Date|method|BASE64|AES|JSON|localStorage|newObject|DES|time|clienttype|pad|appId|timestamp|object|CBC|padding|stringify|Pkcs7|callback|getHours|aes_local_iv|aes_local_key|ObjectSort|null|getTime|24|localStorageUtil|Base64|getDate|setItem|60|current|getValue|oException|getItem||value|dsiY5CDVaHUD|dsk6kDglV7zg|acigqXndJ3AA|success|askMxyuq4bl1|save|console|log|pkKN55abPAHvTT|else|getDataFromLocalStorage|hex_md5|ackRorH6211Q|dgP9mHUUVjCHslg8o0EIwVp|sort|asiEPW7krG2x|Object|keys|map|emhlbnFpcGFsbWl2|xKivqZlVotXWs1rm|encode|h9rMg6p7wIWdgKHa|f551YFGoBX1DCgMw|osEjNiG2Ahx9gfGB|dlon51AU0mAFfFXt|decode|errmsg|errcode|post|b3xHbK6gQslgUx7X|emhlbnFpcGFsbWtleQ|pIhSuWQmTf7cWDTX|dciZS1c8zmuv|dckQy6oOKUho|api|type|hgpBDoQrZ|1000|7b95c6e21fa3b4efabcc2b7d2accd397|WEB|undefined|typeof|secret|removeItem|remove|sGFBGlQSCjdzrohO|check|clear|QuotaExceededError|ajax|catch|try|url|historyapi|php|amSn4Al2QbxUpu9b'.split('|'),0,{}))'''
# encrypted = encrypted.split('}(')[1][:-1]

# print(eval('unpack(' + encrypted))
# print(eval(encrypted))
print(execjs.eval(encrypted))

