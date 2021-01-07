#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import json
import random
import time
import hashlib
from datetime import datetime
from 数据播报.config import settings, send_msg
import urllib3
urllib3.disable_warnings()

url = settings.url
siteId = settings.siteId        # 站点ID
secret = settings.secret
# 对消息进行Base64编码
postBody = json.dumps({
    "template_id":"WORK_TC_APP_1000005",
    "to_users": "fangyu",
    "to_party": "",
    "to_tags": "",
    "to_all": 0,
    # "content": "***会议预订成功通知***\n您的会议室已经预定，稍后会同步到`邮箱`",
    "content": send_msg.content,
    "timestamp": 0,"msg_type": "markdown"})

postBodyMD5 = hashlib.md5(postBody.encode(encoding='UTF-8')).hexdigest()

# 获取当前时间
times = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# 转为时间数组
timeArray = time.strptime(times, "%Y-%m-%d %H:%M:%S")
# 转为时间戳
timestamp = int(time.mktime(timeArray))  # 当前时间戳--整型
# print ("当前时间戳为：",timestamp)
nonceStr = random.randint(9910000, 99100000)  # 随机数
# print ("当前随机数为：",nonceStr)F
signStr = "%s%d%s%s" % (
    postBodyMD5, timestamp, nonceStr, secret)
# print (signStr,type(signStr))
# 进行md5加密
signature = hashlib.md5(signStr.encode(encoding='UTF-8')).hexdigest()
# print (signature,type(signature))

requestURL = "%s?appid=%s&ts=%d&nonce=%s&sign=%s" % (
    url, siteId, timestamp, nonceStr, signature)

headers = {
    "Content-Type": "application/json"
}

# 提交请求
r = requests.post(url=requestURL, headers=headers, data=postBody, verify=False)
resp = json.loads(r.text)
code = resp['code']
msg = resp['msg']
# print(code)
print(msg)

