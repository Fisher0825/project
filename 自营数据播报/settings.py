# --*-- coding: utf-8 --*--
# @Author: Fangyu
# @Email:fangyu@tiancan.tech
# @Time: 2020/11/25 13:58
# @File: seetings.py
import pymysql
conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='qwe123',
    db='yundai',
    charset='utf8'
)
cursor0 = conn.cursor()


conn1 = pymysql.connect(
    host='10.8.91.153',
    port=3306,
    user='tiancanrw',
    password='tiancan#168',
    db='aquarius_ads',
    charset='utf8'
)
cursor1 = conn1.cursor()


url = "https://exchange.tiancan.online/work/v1/send"
siteId = "4JdxC0fPPiXMymC8"        # 站点ID
secret = "MOs5oNGqyPRXtE5j"