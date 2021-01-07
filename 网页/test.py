# --*-- coding: utf-8 --*--
# @Author: Fangyu
# @Email:fangyu@tiancan.tech
# @Time: 2020/12/10 16:02
# @File: sql_test.py

import webbrowser
from 网页 import settings
import time
from dateutil.parser import parse
timestamp_now = int(time.time())#当前时间戳
timeArray_nowtime = time.localtime(timestamp_now)#当前时间戳数组
now_time = time.strftime("%Y-%m-%d %X",timeArray_nowtime)#当前时间
day_time = time.strftime("%Y-%m-%d ",timeArray_nowtime)#当前时间
dt = parse(now_time)
GEN_HTML = "TEST.html"
f = open(GEN_HTML,'w',encoding = 'utf-8')
conn = settings.conn
cursor =settings.cursor
appid = "wxc032de1e8229932a"
# 写入HTML界面中

# sql = """select created_at from wechat_user_base where authorizer_appid = '%s' AND subscribe_count=1 limit 1""" #找到该appid第一次插入数据库的时间
# sql1 = """select created_time from zfb_data where wxid = '%s'limit 1"""%appid #找到该appid第一次插入数据库的时间
sql1 = """select created_at from wechat_user_base 
          where authorizer_appid = '%s' AND subscribe_count=1 limit 1"""%appid #找到该appid第一次插入数据库的时间
cursor.execute(sql1)
tss1 = str(cursor.fetchone()[0])
print(tss1)
if int(tss1) != 0:
    timeArray = time.strptime(tss1, "%Y-%m-%d %H:%M:%S")
    print(timeArray)
    timeStamp = int(time.mktime(timeArray))
    # print(timeStamp)
    sql3 = """SELECT title FROM aquarius_ads.ads_resource 
              where json_contains(config, JSON_OBJECT('authorizer_appid', '%s'));"""%appid
    cursor.execute(sql3)
    nickname = cursor.fetchone()[0]

    #查找总吸粉数
    # sql4 = """select count(distinct openid) from wechat_user_base
    #           where created_at >= '%s-%s-%s 00:00:00' AND authorizer_appid = '%s'
    #           AND subscribe_count=1"""%(timeArray.tm_year,timeArray.tm_mon,timeArray.tm_mday,appid)
    sql4 = """select count(distinct openid) from aquarius_ads.wechat_user_base 
              where openid in(select distinct openid from aquarius_ads.wechat_user_wifi_log 
                              where event in ('subscribe')  and authorizer_appid= '%s') AND created_at >= '%s-%s-%s 00:00:00'"""%\
              (appid, timeArray.tm_year,timeArray.tm_mon,timeArray.tm_mday)
    cursor.execute(sql4)
    total_infans = cursor.fetchone()[0]
    message1 = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <script src="https://cdn.bootcdn.net/ajax/libs/jquery/1.10.0/jquery.min.js"></script>
        <link href="https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/3.4.1/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/3.4.1/js/bootstrap.min.js"></script>
        <meta charset="UTF-8">
        <title>净吸粉数据展示</title>
    </head>
    <body>
    <div class="jumbotron">
    <p>总涨粉量: %s</p>
    <div>
        <div class="layui-table-box">
            <div class="layui-table-header">
                <table cellspacing="0" cellpadding="0" border="0" class="table table-bordered">
                    <thead>
                    <tr>
                        <th data-field="tdate" data-key="3-0-0" class="">
                            <div class="layui-table-cell laytable-cell-3-0-0"><span>日期</span></div>
                        </th>
                        <th data-field="adId" data-key="3-0-1" class="">
                            <div class="layui-table-cell laytable-cell-3-0-1"><span>净吸粉数</span></div>
                        </th>
                        <th data-field="picName" data-key="3-0-5" class="">
                            <div class="layui-table-cell laytable-cell-3-0-5"><span>公众号名称</span></div>
                        </th>
                    </tr>
                    </thead>
    """% total_infans
    message2_1 = """<tbody>"""
    message2 = """ """
    message2_2 = """</tbody>"""
    message3 = """                
        </table>
                </div>
            </div>
        </div>
        </div>
        </body>
    </html>
        """
    while timeStamp < timestamp_now+86400:
        timeArray = time.localtime(timeStamp)
        times = time.strftime("%Y-%m-%d",timeArray)
        print(times)
        # sql2 = """select count(1) from wechat_user_base WHERE created_time <= '%s 23:59:59' AND created_time >= '%s 00:00:00'"""%(times,timestimes,times)
        sql2 = """select count(distinct openid) from aquarius_ads.wechat_user_base 
                 where openid in(select distinct openid from aquarius_ads.wechat_user_wifi_log 
                                 where event in ('subscribe')  and authorizer_appid= '%s') 
                 AND created_time <= '%s 23:59:59' AND created_time >= '%s 00:00:00'"""%(appid,times,times)
        cursor.execute(sql2)
        num = cursor.fetchone()[0]
        message2 += """
                        <tr data-index="0">
                            <td data-field="tdate" data-key="3-0-0">
                                <div class="layui-table-cell laytable-cell-3-0-0"><span>%s</span></div>
                            </td>
                            <td data-field="adId" data-key="3-0-1">
                                <div class="layui-table-cell laytable-cell-3-0-1">%s</div>
                            </td>
                            <td data-field="picName" data-key="3-0-5">
                                <div class="layui-table-cell laytable-cell-3-0-5">%s</div>
                            </td>
                        </tr>
                    """%(times,num,nickname)
        timeStamp += 86400
    cursor.close()
    conn.close()
    # 写入文件
    f.write(message1+message2_1+message2+message2_2+message3)
    # 关闭文件
    f.close()

    # 运行完自动在网页中显示
    webbrowser.open(GEN_HTML, new=1)

else:
    print('数据库中无该公众号吸粉数据')