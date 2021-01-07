# --*-- coding: utf-8 --*--
# @Author: Fangyu
# @Email:fangyu@tiancan.tech
# @Time: 2020/11/24 13:56
# @File: settings.py
import pymysql
# 建立数据库连接
def Conn():
    conn = pymysql.connect(
        # host='10.8.91.153',
        # port=3306,
        # user='tiancanrw',
        # password='tiancan#168',
        # db='aquarius_ads',
        # charset='utf8'
        host='127.0.0.1',
        port=3306,
        user='root',
        password='qwe123',
        db='yundai',
        charset='utf8'
    )
    cursor = conn.cursor()
    return conn,cursor