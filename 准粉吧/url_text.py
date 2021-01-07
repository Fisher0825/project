# --*-- coding: utf-8 --*--
# @Author: Fangyu
# @Email:fangyu@tiancan.tech
# @Time: 2020/11/23 11:36
# @File: test.py
import requests
import json
url = 'https://search-api.shenghuoq.com/dmp-search-api/v4/ad/noauth'
headers = {
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    'Content-Type': "application/json"
}
body = {
    "appNo": "527017ac0142bb93",
    "openId": "oVmEd1HfcTS7TDQIo7-Rwf5ytt8U",
    "facilityId": "95234gd27",
    "userAgent": "Mozilla/5.0 (Linux; Android 7.0; Mi-4c Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN miniProgram",
    "sex": 0,
    "nickname": "1234",
    "creativityType": 1,
    "redirect": ""
}
response = requests.post(url=url, data=json.dumps(body), headers=headers)
# print(content['result']['data'][0])
res = response.json()
obj = res['result']['data'][0]
print(obj)



