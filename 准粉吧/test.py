# --*-- coding: utf-8 --*--
# @Author: Fangyu
# @Email:fangyu@tiancan.tech
# @Time: 2021/1/1 8:19
# @File: test.py
import requests

url = 'https://www.zhunfenba.com/dsp-portal-web/api/open/getAdAuditForChannel'
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
}
data = {
        "appNo": "527017ac0142bb93",
        "page": "1",
        "limit": "10"
}
response = requests.post(url=url, data=data, headers=headers)
res = response.json()['data']
print(res)