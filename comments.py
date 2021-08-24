# 2021/8/24 To_angel

import requests
from Crypto.Cipher import AES
from base64 import b64encode
import json

id = "410181318"  # 歌曲id

url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="  # 评论接口

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
}  # headers伪装

data = {  # 数据
    "csrf_token": "",
    "cursor": "-1",
    "offset": "0",
    "orderType": "1",
    "pageNo": "1",
    "pageSize": "20",
    "rid": "R_SO_4_" + id,
    "threadId": "R_SO_4_" + id,
}

g = "0CoJUm6Qyw8W8jud"  # 定值

i = "BWvA58NO8N91ND3e"  # 变化值，采用其中一个，即此定值


def get_encSecKey():  # 返回encSecKey,根据i计算，i定了，这个也定了
    return "10b1c145c81a7dbc3326b1851c401b34c2bd234b550783014b9e50e47ed1b72a5804396e3cf3be073d6c7356000283f47077d982c4f2ae4ed1e5637ab026dbfb6fc2775c76c340be51297ed5b30a9bed8de2e8680fdfcd9591804245f6cf1253dd7850fa368739f132fc1f7726f8fd185d8978c4777fbd47aa0ad6ef26f9a997"


def get_params(data):  # 接收字符串，返回params
    first = encrypt(data, g)  # 第一次加密
    return encrypt(first, i)  # 第二次加密


def to_16(data):  # 加密前补全16位（加密规则）
    pad = 16 - len(data) % 16
    data += chr(pad) * pad
    return data


def encrypt(data, key):
    IV = "0102030405060708"  # 偏移量
    data = to_16(data)  # 补全
    aes = AES.new(key=key.encode("utf8"), IV=IV.encode("utf8"), mode=AES.MODE_CBC)  # 加密设置
    bs = aes.encrypt(data.encode("utf8"))  # 加密
    return str(b64encode(bs), "utf8")  # 转化成字符串返回


if __name__ == '__main__':
    requests_data = {  # 请求的data（加密后）
        "params": get_params(data=json.dumps(data)),
        "encSecKey": get_encSecKey(),
    }

    resp = requests.post(url=url, headers=headers, data=requests_data)  # post请求

    js = json.loads(resp.text)  # 转为json格式对象

    for i in js.get("data").get("hotComments"):  # 循环输出热评
        print(str(i.get("user").get("nickname")) + "[id:" + str(i.get("user").get("userId")) + "]:" + str(
            i.get("content")))
