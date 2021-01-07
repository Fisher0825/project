# --*-- coding: utf-8 --*--
# @Author: Fangyu
# @Email:fangyu@tiancan.tech
# @Time: 2020/11/26 11:06
# @File: send_msg.py
import time
from dateutil.parser import parse
from 数据播报.config import settings


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

conn = settings.conn
cursor0 = settings.cursor0

conn1 = settings.conn1
cursor1 = settings.cursor1

sql1 = """SELECT SUM(total_fans) FROM `zfb_data` where inserted_time = '%s-%s-%s %s:%s:00'"""% \
       (dt.year,month,dt.day,dt.hour,dt.minute//5*5)
# print(sql1)
cursor0.execute(sql1)
zfb_today_total_infans = cursor0.fetchall()[0][0] #今日总吸粉个数
if zfb_today_total_infans == None:
    zfb_today_total_infans = 0

sql2= """SELECT SUM(total_fans) FROM `zfb_data` where inserted_time = '{}-{}-{} {}:{}:00'""".format\
    (dt_ytd.year,dt_ytd.month,dt_ytd.day,dt_ytd.hour,dt_ytd.minute//5*5)
# print(sql2)
cursor0.execute(sql2)
zfb_ytd_total_infans = cursor0.fetchall()[0][0] #昨日总吸粉个数
if zfb_ytd_total_infans == None:
    zfb_ytd_total_infans = 0

sql3_1 = """SELECT SUM(total_fans) FROM `zfb_data` where inserted_time = '%s-%s-%s %s:%s:00' """%\
         (dt_a5.year,dt_a5.month,dt_a5.day,dt_a5.hour,dt_a5.minute// 5 * 5)

# print(sql3_1)
cursor0.execute(sql3_1)
a = cursor0.fetchall()[0][0]
if a == None:
    a = 0
zfb_today_5min_fans = zfb_today_total_infans-a#最近五分钟吸粉数量

#查询昨日五分钟的吸粉数量
sql4_1 = """SELECT SUM(total_fans) FROM `zfb_data` where inserted_time = '%s-%s-%s %s:%s:00' """%\
         (dt_ya5.year,dt_ya5.month,dt_ya5.day,dt_ya5.hour,dt_ya5.minute// 5 * 5)
sql4_2 = """SELECT SUM(total_fans) FROM `zfb_data` where inserted_time = '%s-%s-%s %s:%s:00'"""%\
         (dt_ya5.year,dt_ya5.month,dt_ytd.day,dt_ya5.hour,dt_ytd.minute// 5 * 5)
cursor0.execute(sql4_1)
a = cursor0.fetchall()[0][0]
if a == None:
    a = 0
cursor0.execute(sql4_2)
b = cursor0.fetchall()[0][0]
if b == None:
    b = 0
zfb_ytd_5min_fans = b-a #昨日五分钟吸粉数量

sql5 = """select count(1) from ads_resource_log  
          where created_at <='%s' and created_at >= '%s' and site_id not in (166565) 
          and location in (40,140) AND advertiser_id=3""" % (now_time, ahead_5m)
# print(sql5)
cursor1.execute(sql5)
# print(cursor1.fetchall()[0][0])
zfb_today_5mout_fans_num = cursor1.fetchall()[0][0]#最近五分钟投放

sql6 = """select count(1) from ads_resource_log  
          WHERE created_at <='%s' and created_at >= '%s' and site_id not in (166565) 
          and location in (40,140) AND advertiser_id=3""" % (ytd_now, ytd_ahead_5m)
cursor1.execute(sql6)
zfb_ytd_5mout_fans_num = cursor1.fetchall()[0][0]#昨日五分钟投放

sql7_1 = """SELECT SUM(total_fans) FROM `zfb_data` 
            where inserted_time = '%s-%s-%s %s:%s:00'"""\
            %(dt_lwa5.year,dt_lwa5.month,dt_lwa5.day,dt_lwa5.hour,dt_lwa5.minute// 5 * 5)#上周同日吸粉总数
sql7_2 = """SELECT SUM(total_fans) FROM `zfb_data` 
            where inserted_time = '%s-%s-%s %s:%s:00'"""\
         %(dt_lw.year,dt_lw.month,dt_lw.day,dt_lw.hour,dt_lw.minute// 5 * 5)#上周同日五分钟前的吸粉总数
cursor0.execute(sql7_1)
zfb_last_week_totalinfans = cursor0.fetchall()[0][0]
if zfb_last_week_totalinfans == None:
    zfb_last_week_totalinfans = 0
cursor0.execute(sql7_2)
b = cursor0.fetchall()[0][0]
if b == None:
    b = 0
zfb_last_week_in_fans = zfb_last_week_totalinfans-b #上周同日五分钟吸粉总数

sql8 = """select count(1) from ads_resource_log  
          where created_at <='%s' and created_at >= '%s' and site_id not in (166565) 
          and location in (40,140) AND advertiser_id=3""" % (last_week, last_week_ahead5)
cursor1.execute(sql8)
zfb_last_week_out_fans = cursor1.fetchall()[0][0] #上周同日五分钟投放总数
# print(zfb_last_week_out_fans,zfb_last_week_out_fans)

sql9 = """SELECT nickName from `zfb_data` 
          WHERE created_time <= '%s' AND created_time >= '%s-%s-%s 00:00:00'"""% (now_time,dt.year,month,day)
# print(sql9)
cursor0.execute(sql9)
data_tup = cursor0.fetchall()
data = []
for i in data_tup:
    if i not in data:
        data.append(i)
# print(data)
content_down = ''

for nickName in data:
    sql10 = """SELECT total_fans from `zfb_data` 
              WHERE inserted_time <= '%s-%s-%s %s:%s:00' 
              AND inserted_time > '%s-%s-%s %s:%s:00' AND nickName = '%s'""" % (
                dt.year,dt.month, dt.day, dt.hour, dt.minute // 5 * 5, dt_a5.year, dt_a5.month,
                dt_a5.day, dt_a5.hour, dt_a5.minute // 5 * 5, nickName[0])
    # print(sql10)
    cursor0.execute(sql10)
    # print(cursor0.execute(sql10))
    zfb_in_num =  cursor0.fetchall()[0][0]#该nickName今日总吸粉数
    # print(in_num)
    sql11 = """SELECT `ghId` from `zfb_data` WHERE nickName = '%s' """%nickName[0]
    cursor0.execute(sql11)
    ghId =cursor0.fetchall()[0][0]
    sql12 = """select count(1) from `ads_resource_log`  
              WHERE created_at <='%s' and created_at >= '%s-%s-%s 00:00:00' and site_id not in (166565) 
              and location in (40,140) AND advertiser_id=3 AND authorizer_username = '%s'""" % (
        now_time,dt.year,dt.month,dt.day,ghId)
    cursor1.execute(sql12)
    zfb_out_num = cursor1.fetchall()[0][0]#该nickName今日总投放数
    if zfb_out_num == 0:
        conver_pec = 1
    else:
        conver_pec = '%.2f' %(zfb_in_num/zfb_out_num*100)
    zfb_in_num = '%-8d'%zfb_in_num
    zfb_out_num = '%-8d'%zfb_out_num
    def strB2q(arg):
        restring = ''
        for i in arg:
            if i != ' ':
                restring += i
            else:
                restring += i*2
        return restring
    zfb_in_num = strB2q(zfb_in_num)
    zfb_out_num = strB2q(zfb_out_num)
    if int(zfb_in_num) != 0 and int(zfb_out_num) != 0:
        content_down = content_down + \
                       '>[{}]：<font color=\"warning\"> {}%</font>\n' \
                       '>=><font color=\"info\">吸: {}净: {}投: {}</font>\n'.format(nickName[0],conver_pec,zfb_in_num,zfb_in_num,zfb_out_num)

#云袋播报数据获取
yd_sql1 = """SELECT SUM(total_fans) FROM `yundai_data` where inserted_time = '%s-%s-%s %s:%s:00'"""% \
       (dt.year,month,dt.day,dt.hour,dt.minute//5*5)
# print(yd_sql1)
cursor0.execute(yd_sql1)
yd_today_total_infans = cursor0.fetchall()[0][0] #今日总吸粉个数
if yd_today_total_infans == None:
    yd_today_total_infans = 0

yd_sql2= """SELECT SUM(total_fans) FROM `yundai_data` where inserted_time = '{}-{}-{} {}:{}:00'""".format\
    (dt_ytd.year,dt_ytd.month,dt_ytd.day,dt_ytd.hour,dt_ytd.minute//5*5)
# print(yd_sql2)
cursor0.execute(yd_sql2)
yd_ytd_total_infans = cursor0.fetchall()[0][0] #昨日总吸粉个数
if yd_ytd_total_infans == None:
    yd_ytd_total_infans = 0

yd_sql3_1 = """SELECT SUM(total_fans) FROM `yundai_data` 
              where inserted_time = '%s-%s-%s %s:%s:00' """%(dt_a5.year,dt_a5.month,dt_a5.day,dt_a5.hour,dt_a5.minute// 5 * 5)
# print(sql3_1)
cursor0.execute(yd_sql3_1)
a = cursor0.fetchall()[0][0]
if a == None:
    a = 0
yd_today_5min_fans = yd_today_total_infans-a#最近五分钟吸粉数量

#查询昨日五分钟的吸粉数量
yd_sql4_1 = """SELECT SUM(total_fans) FROM `yundai_data` 
              where inserted_time = '%s-%s-%s %s:%s:00' """%(dt_ya5.year,dt_ya5.month,dt_ya5.day,dt_ya5.hour,dt_ya5.minute// 5 * 5)
yd_sql4_2 = """SELECT SUM(total_fans) FROM `yundai_data` 
              where inserted_time = '%s-%s-%s %s:%s:00'"""%(dt_ya5.year,dt_ya5.month,dt_ytd.day,dt_ya5.hour,dt_ytd.minute// 5 * 5)
cursor0.execute(yd_sql4_1)
a = cursor0.fetchall()[0][0]
if a == None:
    a = 0
cursor0.execute(yd_sql4_2)
b = cursor0.fetchall()[0][0]
if b == None:
    b = 0
yd_ytd_5min_fans = b-a #昨日五分钟吸粉数量

yd_sql5 = """select count(1) from ads_resource_log  
          where created_at <='%s' and created_at >= '%s' and site_id not in (166565) 
          and location in (40,140) AND advertiser_id=2""" % (now_time, ahead_5m)
# print(yd_sql5)
cursor1.execute(yd_sql5)
yd_today_5mout_fans_num = cursor1.fetchall()[0][0]
yd_sql6 = """select count(1) from ads_resource_log  
            WHERE created_at <='%s' and created_at >= '%s' and site_id not in (166565) 
            and location in (40,140) AND advertiser_id=2""" % (ytd_now, ytd_ahead_5m)
cursor1.execute(yd_sql6)
yd_ytd_5mout_fans_num = cursor1.fetchall()[0][0]

yd_sql7_1 = """SELECT SUM(total_fans) FROM `yundai_data` 
            where inserted_time = '%s-%s-%s %s:%s:00'"""\
            %(dt_lwa5.year,dt_lwa5.month,dt_lwa5.day,dt_lwa5.hour,dt_lwa5.minute// 5 * 5)
yd_sql7_2 = """SELECT SUM(total_fans) FROM `yundai_data` 
            where inserted_time = '%s-%s-%s %s:%s:00'"""\
            %(dt_lw.year,dt_lw.month,dt_lw.day,dt_lw.hour,dt_lw.minute// 5 * 5)#云袋上周同日吸粉总数
cursor0.execute(yd_sql7_1)
a = cursor0.fetchall()[0][0]
if a == None:
    a = 0
cursor0.execute(yd_sql7_2)
yd_last_week_totalinfans = cursor0.fetchall()[0][0]
if yd_last_week_totalinfans == None:
    yd_last_week_totalinfans = 0
yd_last_week_in_fans = yd_last_week_totalinfans-a #上周同日五分钟吸粉总数

yd_sql8 = """select count(1) from ads_resource_log  
          where created_at <='%s' and created_at >= '%s' and site_id not in (166565) 
          and location in (40,140) AND advertiser_id=2""" % (last_week, last_week_ahead5)
cursor1.execute(yd_sql8)
yd_last_week_out_fans = cursor1.fetchall()[0][0] #上周同日五分钟投放总数

yd_sql9 = """SELECT nickName from `yundai_data` 
          WHERE created_time <= '%s' AND created_time >= '%s-%s-%s 00:00:00'"""% (now_time,dt.year,month,day)
cursor0.execute(yd_sql9)
data_tup = cursor0.fetchall()
data = []
for i in data_tup:
    if i not in data:
        data.append(i)
yd_content = ''
for nickName in data:
    dt_a5.minute//5 * 5
    yd_sql10 = """SELECT total_fans from `yundai_data` 
                  WHERE inserted_time <= '%s-%s-%s %s:%s:00' 
                  AND inserted_time > '%s-%s-%s %s:%s:00' AND nickName = '%s'""" % (
            dt.year,dt.month, dt.day, dt.hour, dt.minute // 5 * 5,
            dt_a5.year,dt_a5.month, dt_a5.day, dt_a5.hour, dt_a5.minute // 5 * 5, nickName[0])
    cursor0.execute(yd_sql10)
    yd_in_num =  cursor0.fetchall()[0][0]#该nickName今日总吸粉数
    yd_sql11 = """SELECT `wxId` from `yundai_data` WHERE nickName = '%s' """%nickName[0]
    cursor0.execute(yd_sql11)
    wxId =cursor0.fetchall()[0][0]
    yd_sql12 = """select count(1) from `ads_resource_log`  
                WHERE created_at <='%s' and created_at >= '%s-%s-%s 00:00:00' and site_id 
                not in (166565) and location in (40,140) AND advertiser_id=2 
                AND authorizer_appid = '%s'""" % (now_time,dt.year,dt.month,dt.day,wxId)
    cursor1.execute(yd_sql12)
    yd_out_num = cursor1.fetchall()[0][0]#该nickName今日总投放数
    if yd_out_num == 0:
        yd_conver_pec = 1
    else:
        yd_conver_pec = '%.2f' %(yd_in_num/yd_out_num*100)
    yd_in_num = '%-8d'%yd_in_num
    yd_out_num = '%-8d'%yd_out_num
    def strB2q(arg):
        restring = ''
        for i in arg:
            if i != ' ':
                restring += i
            else:
                restring += i*2
        return restring
    yd_in_num = strB2q(yd_in_num)
    yd_out_num = strB2q(yd_out_num)
    yd_content = yd_content+'>[{}]：<font color=\"warning\"> {}%</font>\n' \
                   '>=><font color=\"info\">吸: {}净: {}投: {}</font>\n'.format(nickName[0],yd_conver_pec,yd_in_num,yd_in_num,yd_out_num)

#自营数据播报
zy_sql1 = """select count(1) from wechat_user_wifi_log  
          where created_at <= '%s' AND created_at >= '%s-%s-%s 00:00:00' 
          AND source_type=1 and `event` in ('subscribe') """%\
       (now_time,dt.year,dt.month,dt.day)#自营今日吸粉总数
# print(sql1)
cursor1.execute(zy_sql1)
zy_today_total_infans = cursor1.fetchall()[0][0] #今日总吸粉个数
# print(today_total_infans)

zy_sql2 = """select count(1) from wechat_user_wifi_log  
          where created_at <= '%s' AND created_at >= '%s-%s-%s 00:00:00' 
          AND source_type=1 and `event` in ('subscribe') """%\
       (ytd_now,dt_ytd.year,dt_ytd.month,dt_ytd.day)#自营昨日吸粉
# print(sql2)
cursor1.execute(zy_sql2)
zy_ytd_total_infans = cursor1.fetchall()[0][0] #昨日总吸粉个数
if zy_ytd_total_infans == None:
    ytd_total_infans = 0
# print(ytd_total_infans)

zy_sql3 = """select count(1) from ads_resource_log  
          where created_at <='%s' and created_at >= '%s' 
          and site_id not in (166565) 
          and location in (40,140) AND advertiser_id=1""" % \
       (now_time, ahead_5m)#最近五分钟投放
# print(sql3)
cursor1.execute(zy_sql3)
zy_today_5mout_fans_num = cursor1.fetchall()[0][0]#最近五分钟投放
# print(today_5mout_fans_num)

zy_sql4 = """select count(1) from wechat_user_wifi_log  
          where created_at <= '%s' AND created_at >= '%s' AND source_type=1 
          and `event` in ('subscribe') """%\
       (now_time, ahead_5m)#最近五分钟吸粉
# print(sql4)
cursor1.execute(zy_sql4)
zy_today_5min_fans = cursor1.fetchall()[0][0]#最近五分钟吸粉
# print(today_5min_fans)

zy_sql5 = """select count(1) from ads_resource_log  
          WHERE created_at <='%s' and created_at >= '%s' 
          and site_id not in (166565) and location in (40,140) 
          AND advertiser_id=1""" % \
       (ytd_now, ytd_ahead_5m)#昨日五分钟投放
# print(sql5)
cursor1.execute(zy_sql5)
zy_ytd_5mout_fans_num = cursor1.fetchall()[0][0]#昨日五分钟投放
# print(ytd_5mout_fans_num)

zy_sql6 = """select count(1) from wechat_user_wifi_log  
          where created_at <= '%s' AND created_at >= '%s' AND source_type=1 
          and `event` in ('subscribe') """%\
       (ytd_now, ytd_ahead_5m) #昨日五分钟吸粉
# print(sql6)
cursor1.execute(zy_sql6)
zy_ytd_5min_fans = cursor1.fetchall()[0][0]#昨日五分钟吸粉
# print(ytd_5min_fans)

zy_sql7 = """select count(1) from ads_resource_log  
          WHERE created_at <='%s' and created_at >= '%s' and site_id not in (166565) 
          and location in (40,140) AND advertiser_id=1""" % \
       (last_week, last_week_ahead5)#上周同日五分钟投放
# print(sql7)
cursor1.execute(zy_sql7)
zy_last_week_out_fans = cursor1.fetchall()[0][0] #上周同日五分钟投放总数
# print(last_week_out_fans)
#
zy_sql8 = """select count(1) from wechat_user_wifi_log  
          where created_at <= '%s' AND created_at >= '%s' 
          AND source_type=1 and `event` in ('subscribe') """%\
       (last_week, last_week_ahead5) #上周同日五分钟吸粉
# print(sql8)
cursor1.execute(zy_sql8)
zy_last_week_in_fans = cursor1.fetchall()[0][0] #上周同日五分钟吸粉总数
# print(last_week_in_fans)

zy_content_up = "\n**---------------------**\n" \
                "### <font color=\"info\">自营数据播报</font>\n" \
                "\n**---------------------**\n"\
                ">自营今日吸粉：%s 个\n" \
                ">自营昨日吸粉：%s 个\n" \
                ">最近5分钟投放：%s 个\n" \
                ">最近5分钟吸粉：%s 个\n" \
                ">昨日5分钟投放：%s 个\n" \
                ">昨日5分钟吸粉：%s 个\n" \
                ">上周同日5分钟投放：%s 个\n" \
                ">上周同日5分钟吸粉：%s 个\n" \
                "-----自营吸粉明细-----\n"%(zy_today_total_infans,
                                zy_ytd_total_infans,zy_today_5mout_fans_num,
                                zy_today_5min_fans,zy_ytd_5mout_fans_num,zy_ytd_5min_fans,
                                zy_last_week_out_fans,zy_last_week_in_fans)
zysql9 = """select distinct `resource_title` from ads_resource_log a,ads_resource b  
            where a.created_at <='%s' and a.created_at >= '%s-%s-%s 00:00:00' 
            and a.site_id not in (166565) and a.location in (40,140) AND a.advertiser_id=1 
            and b.pid=1 and resource_title=b.title"""%\
            (now_time, dt.year, dt.month, dt.day)
cursor1.execute(zysql9)
ziyin_titles = cursor1.fetchall()#找出当日投放的所有自营号的名称
# print(ziyin_titles)

zy_sql14 = """select count(1) from wechat_user_wifi_log  
          where created_at <= '%s' AND created_at >= '%s-%s-%s 00:00:00' 
          AND source_type=1 and `event` in ('subscribe') """%(last_week,dt_lw.year,dt_lw.month,dt_lw.day)#自营上周同日吸粉总数
cursor1.execute(zy_sql14)
zy_last_week_total_infans = cursor1.fetchall()[0][0]


zy_content_down = ''
for title in ziyin_titles:
    zysql10 = """select DISTINCT `authorizer_appid` from ads_resource_log  
                where created_at <='%s' and created_at >= '%s-%s-%s 00:00:00' 
                and site_id not in (166565) and location in (40,140) 
                AND advertiser_id=1 AND resource_title = '%s'"""%\
           (now_time, dt.year, dt.month, dt.day,title[0])#找出对应title的对应appid
    # print(zysql10)
    cursor1.execute(zysql10)
    ziyin_appid = cursor1.fetchall()[0][0]
    # print(ziyin_appid)
    zysql11 = """select count(1) from wechat_user_wifi_log  
                where created_at <= '%s' AND created_at >= '%s-%s-%s 00:00:00' 
                AND source_type=1 and `event` in ('subscribe') 
                AND authorizer_appid = '%s'"""%\
            (now_time, dt.year, dt.month, dt.day,ziyin_appid) #找出当日该自营号的吸粉数量
    # print(zysql11)
    cursor1.execute(zysql11)
    # print(cursor1.fetchone())
    zy_today_in_num = cursor1.fetchone()
    if zy_today_in_num == None:
        zy_today_in_num = (0,)
    zysql12 = """select count(distinct openid) from wechat_user_base where created_at <='%s' and created_at >= '%s-%s-%s 00:00:00' AND authorizer_appid = '%s' AND subscribe_count=1"""%(now_time, dt.year, dt.month, dt.day,ziyin_appid)
    cursor1.execute(zysql12)
    # print(cursor1.fetchone())
    zy_today_net_num = cursor1.fetchone()#净增
    if zy_today_net_num == None:
        zy_today_net_num = (0,)

    zysql13 = """select count(1) from ads_resource_log  
                where created_at <='%s' and created_at >= '%s-%s-%s 00:00:00' 
                and site_id not in (166565) and location in (40,140) AND advertiser_id=1 
                AND resource_title = '%s'"""%\
            (now_time, dt.year, dt.month, dt.day,title[0])
    cursor1.execute(zysql13)
    # print(cursor1.fetchone())#投放数
    zy_today_out_num = cursor1.fetchone()
    if zy_today_out_num == None:
        zy_today_out_num = (0,)
    if zy_today_out_num == (0,):
        zy_conver_pec = 1
    else:
        zy_conver_pec = '%.2f' %(zy_today_in_num[0]/zy_today_out_num[0]*100)

    zy_today_in_num = '%-6d'%zy_today_in_num[0]
    zy_today_net_num = '%-6d'%zy_today_net_num[0]
    zy_today_out_num = '%-6d'%zy_today_out_num[0]
    def strB2q(arg):
        restring = ''
        for i in arg:
            if i != ' ':
                restring += i
            else:
                restring += i*2
        return restring
    zy_today_in_num = strB2q(zy_today_in_num)
    zy_today_net_num = strB2q(zy_today_net_num)
    zy_today_out_num = strB2q(zy_today_out_num)
    zy_content_down += ">[自授权][{}]:转：<font color=\"warning\"> {}%</font>\n" \
                        ">=><font color=\"info\">吸：{}净增：{}投：{}</font>\n"\
        .format(title[0] , zy_conver_pec, zy_today_in_num, zy_today_net_num, zy_today_out_num)
zy_content = zy_content_up + zy_content_down

yd_content_down = '\n**---------------------**\n' \
                  '### <font color=\"info\">云袋数据播报</font>' \
                  '\n**---------------------**\n' \
                  '>今日吸粉：{}个\n' \
                  '>昨日吸粉： {}个\n' \
                  '>最近5分钟投放： {}个 \n' \
                  '>最近5分钟吸粉： {} 个 \n' \
                  '\n'.format(yd_today_total_infans,yd_ytd_total_infans,
                              yd_today_5mout_fans_num,yd_today_5min_fans)+ yd_content

content_up =  "### **吸粉数据播报:**" \
              "\n[%s]\n" \
              ">今日吸粉：%s个\n" \
              ">昨日吸粉：%s个\n" \
              ">最近5分钟投放：%s个 \n" \
              ">最近5分钟吸粉：%s 个 \n" \
              ">昨日5分钟投放：%s 个 \n" \
              ">昨日5分钟吸粉：%s 个 \n" \
              "上周同日吸粉：%s 个\n"\
              ">上周同日5分钟投放： %s 个\n" \
              ">上周同日5分钟吸粉： %s 个 \n" \
              " \n" \
              "**---------------------**\n" \
              "### <font color=\"info\">准粉吧数据播报</font>\n" \
              "**---------------------**\n" \
              ">今日吸粉：%s个\n" \
              ">昨日吸粉：%s个\n" \
              ">最近5分钟投放：%s个 \n" \
              ">最近5分钟吸粉：%s 个 \n" \
              "\n"%\
             (date_time,zfb_today_total_infans+yd_today_total_infans+zy_today_total_infans,
              zfb_ytd_total_infans+yd_ytd_total_infans+zy_ytd_total_infans,
              zfb_today_5mout_fans_num+yd_today_5mout_fans_num+zy_today_5mout_fans_num,
              zfb_today_5min_fans+yd_today_5min_fans+zy_today_5min_fans,
              zfb_ytd_5mout_fans_num+yd_ytd_5mout_fans_num+zy_ytd_5mout_fans_num,
              zfb_ytd_5min_fans+yd_ytd_5min_fans+zy_ytd_5min_fans,
              zfb_last_week_totalinfans+yd_last_week_totalinfans+zy_last_week_total_infans,
              zfb_last_week_out_fans+yd_last_week_out_fans+zy_last_week_out_fans,
              zfb_last_week_in_fans+yd_last_week_in_fans+zy_last_week_in_fans,
              zfb_today_total_infans,zfb_ytd_total_infans,zfb_today_5mout_fans_num,zfb_today_5min_fans)

ziyin_contont = '\n**---------------------**\n' \
                '### <font color=\"info\">自营数据播报</font>' \
                '\n**---------------------**\n' \

content = content_up+content_down+yd_content_down +zy_content
cursor0.close()
conn.close()
cursor1.close()
conn1.close()




