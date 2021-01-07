# --*-- coding: utf-8 --*--
# @Author: Fangyu
# @Email:fangyu@tiancan.tech
# @Time: 2020/12/2 17:15
# @File: send_msg.py
import time
from dateutil.parser import parse
from 自营数据播报 import settings

timesramp = int(time.time())#当前时间戳
timeArray_nowtime = time.localtime(timesramp)#当前时间戳
timeArray_5miu = time.localtime(int(time.time()-300))#当前时间五分钟之前的时间戳
timeArray_ytd_now = time.localtime(int(time.time()-86400))#当前时间前一天的时间戳
timeArray_ytd_ahead_5m = time.localtime(int(time.time()-86700))#当前时间前一天五分钟前的时间戳
timeArray_last_week = time.localtime(int(time.time()-604800))#当前时间一个礼拜前的时间戳
timeArray_last_week_ahead5 = time.localtime(int(time.time()-605100))#当前时间一个礼拜再往前五分钟前的时间戳
# search_time = time.strftime("%Y-%m-%d %H:{}:00".format(dt.minute // 5 * 5))
now_time = time.strftime("%Y-%m-%d %X",timeArray_nowtime)#当前时间
ahead_5m = time.strftime("%Y-%m-%d %X",timeArray_5miu)#当前时间五分钟之前的时间
ytd_now = time.strftime("%Y-%m-%d %X",timeArray_ytd_now)#当前时间前一天的时间
ytd_ahead_5m = time.strftime("%Y-%m-%d %X",timeArray_ytd_ahead_5m)#当前时间前一天五分钟前
last_week = time.strftime("%Y-%m-%d %X",timeArray_last_week)#当前时间一个礼拜再往前五分钟前的时间
last_week_ahead5 = time.strftime("%Y-%m-%d %X",timeArray_last_week_ahead5)
dt = parse(now_time)
month = dt.month
day = dt.day
hour = dt.hour
minute = dt.minute // 5 * 5 #当前时间分钟的整除分钟
dt_a5 = parse(ahead_5m)
dt_ytd = parse(ytd_now)
dt_ya5 = parse(ytd_ahead_5m)
dt_lw = parse(last_week)
dt_lwa5 = parse(last_week_ahead5)
if dt.minute<10:
    date_time = time.strftime("%Y-%m-%d %H:0{}".format(dt.minute//5*5))
else:
    date_time = time.strftime("%Y-%m-%d %H:{}".format(dt.minute // 5 * 5))

conn1 = settings.conn1
cursor1 = settings.cursor1

sql1 = """select count(1) from wechat_user_wifi_log  where created_at <= '%s' AND created_at >= '%s-%s-%s 00:00:00' AND source_type=1 and `event` in ('subscribe') """%\
       (now_time,dt.year,dt.month,dt.day)#自营今日吸粉总数
# print(sql1)
cursor1.execute(sql1)
today_total_infans = cursor1.fetchall()[0][0] #今日总吸粉个数
# print(today_total_infans)

sql2 = """select count(1) from wechat_user_wifi_log  where created_at <= '%s' AND created_at >= '%s-%s-%s 00:00:00' AND source_type=1 and `event` in ('subscribe') """%\
       (ytd_now,dt_ytd.year,dt_ytd.month,dt_ytd.day)#自营昨日吸粉
# print(sql2)
cursor1.execute(sql2)
ytd_total_infans = cursor1.fetchall()[0][0] #昨日总吸粉个数
if ytd_total_infans == None:
    ytd_total_infans = 0
# print(ytd_total_infans)

sql3 = """select count(1) from ads_resource_log  where created_at <='%s' and created_at >= '%s' and site_id not in (166565) and location in (40,140) AND advertiser_id=1""" % \
       (now_time, ahead_5m)#最近五分钟投放
# print(sql3)
cursor1.execute(sql3)
today_5mout_fans_num = cursor1.fetchall()[0][0]#最近五分钟投放
# print(today_5mout_fans_num)

sql4 = """select count(1) from wechat_user_wifi_log  where created_at <= '%s' AND created_at >= '%s' AND source_type=1 and `event` in ('subscribe') """%\
       (now_time, ahead_5m)#最近五分钟吸粉
# print(sql4)
cursor1.execute(sql4)
today_5min_fans = cursor1.fetchall()[0][0]#最近五分钟吸粉
# print(today_5min_fans)

sql5 = """select count(1) from ads_resource_log  WHERE created_at <='%s' and created_at >= '%s' and site_id not in (166565) and location in (40,140) AND advertiser_id=1""" % \
       (ytd_now, ytd_ahead_5m)#昨日五分钟投放
# print(sql5)
cursor1.execute(sql5)
ytd_5mout_fans_num = cursor1.fetchall()[0][0]#昨日五分钟投放
# print(ytd_5mout_fans_num)

sql6 = """select count(1) from wechat_user_wifi_log  where created_at <= '%s' AND created_at >= '%s' AND source_type=1 and `event` in ('subscribe') """%\
       (ytd_now, ytd_ahead_5m) #昨日五分钟吸粉
# print(sql6)
cursor1.execute(sql6)
ytd_5min_fans = cursor1.fetchall()[0][0]#昨日五分钟吸粉
# print(ytd_5min_fans)

sql7 = """select count(1) from ads_resource_log  WHERE created_at <='%s' and created_at >= '%s' and site_id not in (166565) and location in (40,140) AND advertiser_id=1""" % \
       (last_week, last_week_ahead5)#上周同日五分钟投放
# print(sql7)
cursor1.execute(sql7)
last_week_out_fans = cursor1.fetchall()[0][0] #上周同日五分钟投放总数
# print(last_week_out_fans)
#
sql8 = """select count(1) from wechat_user_wifi_log  where created_at <= '%s' AND created_at >= '%s' AND source_type=1 and `event` in ('subscribe') """%\
       (last_week, last_week_ahead5) #上周同日五分钟吸粉
# print(sql8)
cursor1.execute(sql8)
last_week_in_fans = cursor1.fetchall()[0][0] #上周同日五分钟投放总数
# print(last_week_in_fans)

zy_content_up = "### **======自营数据播报=====**:\n" \
          "[%s]\n" \
          "自营今日吸粉: %s 个\n" \
          "自营昨日吸粉: %s 个\n" \
          "最近5分钟投放: %s 个\n" \
          "最近5分钟吸粉: %s 个\n" \
          "昨日5分钟投放: %s 个\n" \
          "昨日5分钟吸粉: %s 个\n" \
          "上周同日5分钟投放: %s 个\n" \
          "上周同日5分钟吸粉: %s 个\n" \
          "-----自营吸粉明细-----\n"%(date_time,today_total_infans,ytd_total_infans,today_5mout_fans_num,today_5min_fans,ytd_5mout_fans_num,ytd_5min_fans,last_week_out_fans,last_week_in_fans)

zy_content_down = ''
zysql9 = """select `resource_title` from ads_resource_log  where created_at <='%s' and created_at >= '%s-%s-%s 00:00:00' and site_id not in (166565) and location in (40,140) AND advertiser_id=1 """%\
       (now_time, dt.year, dt.month, dt.day)
cursor1.execute(zysql9)
ziyin_titles = cursor1.fetchall()#找出当日投放的所有自营号的名称
ziyin_title_list = []
for i in ziyin_title_list:
    if i not in ziyin_title:
        data.append(i)
for title in ziyin_titles:
    zysql10 = """select `authorizer_appid` from ads_resource_log  where created_at <='%s' and created_at >= '%s-%s-%s 00:00:00' and site_id not in (166565) and location in (40,140) AND advertiser_id=1 AND resource_title = '%s'"""%\
           (now_time, dt.year, dt.month, dt.day,title[0])#找出对应title的对应appid
    cursor1.execute(zysql10)
    ziyin_appid = cursor1.fetchall()[0][0]
    zysql11 = """select count(1) from wechat_user_wifi_log  where created_at <= '%s' AND created_at >= '%s-%s-%s 00:00:00' AND source_type=1 and `event` in ('subscribe') AND authorizer_appid = '%s'"""%\
            (now_time, dt.year, dt.month, dt.day,ziyin_appid) #找出当日该自营号的吸粉数量
    cursor1.execute(zysql11)
    zy_today_in_num = cursor1.fetchone()[0][0]
    zysql12 = """select count(1) from wechat_user_base where authorizer_appid = '%s' AND subscribe_count=1 """%(ziyin_appid)
    cursor1.execute(zysql12)
    zy_today_net_num = cursor1.fetchone()[0][0] #净增长数
    zysql13 = """select count(1) from ads_resource_log  where created_at <='%s' and created_at >= '%s-%s-%s 00:00:00' and site_id not in (166565) and location in (40,140) AND advertiser_id=1 AND resource_title = '%s'"""%\
            (now_time, dt.year, dt.month, dt.day,title[0])
    cursor1.execute()
    zy_today_out_num = cursor1.fetchone()[0][0]
    if zy_today_out_num == 0:
        zy_conver_pec = 1
    else:
        zy_conver_pec = '%.2f' %(zy_today_in_num/zy_today_out_num*100)
    zy_content_down += "[自授权][%s]:\n"+\
                    "=>吸：%s     净增：%s     投： %s     转：%s\n"% (zy_today_in_num, zy_today_net_num, zy_today_out_num, zy_conver_pec)
content = zy_content_up + zy_content_down