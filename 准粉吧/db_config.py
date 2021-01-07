# --*-- coding: utf-8 --*--
# @Author: Fangyu
# @Email:fangyu@tiancan.tech
# @Time: 2020/11/23 12:03
# @File: db_config.py
import pymysql
import json
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
# 获取游标
cursor = conn.cursor()
# sql = """alter table `ads_resource` AUTO_INCREMENT=6;"""
# cursor.execute(sql)
# 查出pid=2的config字段列的所有数据
# sql = """select config from ads_resource WHERE pid=3 """
# rows = cursor.execute(sql)
# config_tups = cursor.fetchall()
# print(json.loads(config_tups[0][0]))

sql = """select `check_times` from `zhunfenba_extra` WHERE appid='wx5426eabc7df04b85'"""
cursor.execute(sql)
check_times = cursor.fetchone()
print(check_times)