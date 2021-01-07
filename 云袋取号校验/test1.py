import requests,json
import pymysql
from io import BytesIO
from pyzbar import pyzbar
from PIL import Image, ImageEnhance

#
url = 'http://api.goluodi.com/shunwang/gettask?SenceId=223.196.75.106=&areacode&business_type=2'
#先从接口中拿到所有appid的信息
response = requests.get(url=url)
page_text = response.text
# with open('test.txt','w',encoding='utf-8') as fp:
#     fp.write(page_text)
res = response.json()
print(res)

