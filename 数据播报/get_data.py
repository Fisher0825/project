# --*-- coding: utf-8 --*--
# @Author: Fangyu
# @Email:fangyu@tiancan.tech
# @Time: 2020/11/25 15:20
# @File: get_data.py
import requests,time
from dateutil.parser import parse
from config import settings

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
# print(response.json())
conn = settings.conn
cursor = settings.cursor0
for data in res:
    now_time = time.strftime("%Y-%m-%d %H:%M:%S")
    dt = parse(now_time)
    inserted_time = time.strftime("%Y-%m-%d %H:{}:00".format(dt.minute // 5 * 5))
    # print(inserted_time)
    if str(data['todayClick']) in str(data):
        if data['todayClick'] != 0:
            sql = """ INSERT INTO `zfb_data`(`nickName`, `wxId`, `adId`, `total_fans`, `created_time`, `inserted_time`, `ghId`) VALUES ('%s','%s','%s','%s','%s','%s','%s')"""%(data['adName'],data['wxId'],data['adId'],data['todayClick'],now_time,inserted_time,data['ghId'])
            # print(sql)
            cursor.execute(sql)
            conn.commit()
        elif data['todayClick'] == 0:
            sql = """ INSERT INTO `zfb_data`(`nickName`, `wxId`, `adId`, `total_fans`, `created_time`, `inserted_time`, `ghId`) VALUES ('%s','%s','%s','%s','%s','%s','%s')""" % (
            data['adName'], data['wxId'], data['adId'], data['todayClick'], now_time, inserted_time, data['ghId'])
            # print(sql)
            cursor.execute(sql)
            conn.commit()
print('准粉吧数据插入成功')



conn = settings.conn
cursor = settings.cursor0
ti = time.strftime('%Y-%m-%d')
addr_list = ['shunwang','lianwo']
for addr in addr_list:
    url = "http://api.goluodi.com/%s/get_data?date=%s"%(addr,ti)
    response = requests.get(url=url)
    if addr == 'lianwo':
        if 'data' in response.json():
            res = response.json()['data']
            conn = settings.conn
            cursor = settings.cursor0
            for data in res:
                now_time = time.strftime("%Y-%m-%d %H:%M:%S")
                dt = parse(now_time)
                inserted_time = time.strftime("%Y-%m-%d %H:{}:00".format(dt.minute // 5 * 5))
                if data['follow']:
                    sql = """ INSERT INTO `yundai_data`(`nickName`, `wxId`, `total_fans`, `created_time`, `inserted_time`) VALUES ('%s','%s','%s','%s','%s')"""%(data['wx_name'],data['appid'],data['follow'],now_time,inserted_time)
                    cursor.execute(sql)
                    conn.commit()
            print('连我数据已插入')
        else:
            print('连我没有数据')
    else:
        res = response.json()['data']
        # print(res)
        conn = settings.conn
        cursor = settings.cursor0
        for data in res:
            now_time = time.strftime("%Y-%m-%d %H:%M:%S")
            dt = parse(now_time)
            inserted_time = time.strftime("%Y-%m-%d %H:{}:00".format(dt.minute // 5 * 5))
            if data['follow']:
                sql = """ INSERT INTO `yundai_data`(`nickName`, `wxId`, `total_fans`, `created_time`, `inserted_time`) VALUES ('%s','%s','%s','%s','%s')""" % (
                data['wx_name'], data['appid'], data['follow'], now_time, inserted_time)
                cursor.execute(sql)
                conn.commit()
cursor.close()
conn.close()
print('云袋数据插入成功')




#

