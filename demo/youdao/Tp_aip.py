
#coding=utf8

# import httplib
# import md5
import urllib
import requests
import hashlib
import random
import json
import base64
from dj import settings

# 您的应用ID
appKey = settings.appKey
# 您的应用密钥，请勿把它和appKey泄露给他人
appSecret = settings.appSecret

url = 'http://openapi.youdao.com/ocrtransapi'

def get_trans(image_path):

    httpClient = None

    try:

        # 参数部分
        with open(image_path, 'rb') as f:
            q = base64.b64encode(f.read()).decode('utf-8')
        # f = open('1.png', 'rb') #二进制方式打开图文件
        # q = base64.b64encode(f.read()).decode('utf-8') #读取文件内容，转换为base64编码
        # f.close()
        # 源语言
        fromLan = "auto"
        # 目标语言
        to = "zh-CHS"
        # 上传类型
        type = "1"
        # 随机数，自己随机生成，建议时间戳
        salt = random.randint(1, 65536)
        # 签名
        sign = appKey+q+str(salt)+appSecret
        m1 = hashlib.md5()
        m1.update(sign.encode('utf-8'))
        sign = m1.hexdigest()
        data = {'appKey': appKey, 'q': q, 'from': fromLan, 'to': to, 'type': type, 'salt': str(salt), 'sign': sign}
        #data = urllib.parse.urlencode(data)
        res = requests.post(url=url, data=data)
        # req = urllib2.Request('http://openapi.youdao.com/ocrtransapi',data)
        #response是HTTPResponse对象
        # response = urllib2.urlopen(req)
        # print(response.read())
        ret = json.loads(res.content.decode('utf-8'))
        return ret['resRegions']
    except Exception as e:
        return e
    finally:
        if httpClient:
            httpClient.close()