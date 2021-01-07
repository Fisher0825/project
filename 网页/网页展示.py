# --*-- coding: utf-8 --*--
# @Author: Fangyu
# @Email:fangyu@tiancan.tech
# @Time: 2020/12/10 9:39
# @File: 网页展示.py
import webbrowser
from 网页 import settings
import time
from dateutil.parser import parse
timesramp = int(time.time())#当前时间戳
timeArray_nowtime = time.localtime(timesramp)#当前时间戳
now_time = time.strftime("%Y-%m-%d %X",timeArray_nowtime)#当前时间
day_time = time.strftime("%Y-%m-%d ",timeArray_nowtime)#当前时间
dt = parse(now_time)
GEN_HTML = "TEST.html"
f = open(GEN_HTML,'w',encoding = 'utf-8')

conn = settings.conn
cursor =settings.cursor
appid = "wxc032de1e8229932a"
# sql = """select created_at from wechat_user_base where authorizer_appid = '%s' AND subscribe_count=1 limit 1""" #找到该appid第一次插入数据库的时间
sql = """select created_time from zfb_data where wxId = '%s'limit 1"""%appid #找到该appid第一次插入数据库的时间
cursor.execute(sql)
# zysql12 = """select count(distinct openid) from wechat_user_base where created_at <='%s' and created_at >= '%s-%s-%s 00:00:00' AND authorizer_appid = '%s' AND subscribe_count=1"""%(now_time, dt.year, dt.month, dt.day,appid)
cursor.execute(sql)
zy_today_net_num = cursor.fetchone()#净增
if zy_today_net_num == None:
    zy_today_net_num = (0,)

# 写入HTML界面中
message1 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <script src="https://cdn.bootcdn.net/ajax/libs/jquery/1.10.0/jquery.min.js"></script>
    <link href="https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/3.4.1/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/3.4.1/js/bootstrap.min.js"></script>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<div class="jumbotron">
<p>401</p>
<p>总涨粉量</p>
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
                </thead>"""
message2_1 = """<tbody>"""
message2 = """
                
                <tr data-index="0" class="">
                    <td data-field="tdate" data-key="3-0-0" class="">
                        <div class="layui-table-cell laytable-cell-3-0-0"><span>%s</span></div>
                    </td>
                    <td data-field="adId" data-key="3-0-1" class="">
                        <div class="layui-table-cell laytable-cell-3-0-1">%s</div>
                    </td>
                    <td data-field="picName" data-key="3-0-5" class="">
                        <div class="layui-table-cell laytable-cell-3-0-5">爱华夏高铁2</div>
                    </td>
                </tr>
                </tbody>
            </table>
        </div>
    </div>

    <nav aria-label="Page navigation">
      <ul class="pagination text-center" >
        <li>
          <a href="#" aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
          </a>
        </li>
        <li class="active"><a href="#">1 <span class="sr-only">(current)</span></a></li>
        <li><a href="#">2</a></li>
        <li><a href="#">3</a></li>
        <li><a href="#">4</a></li>
        <li><a href="#">5</a></li>
        <li>
          <a href="#" aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
          </a>
        </li>
      </ul>
    </nav>
</div>
</div>
</body>
</html>
"""%(day_time,zy_today_net_num[0])

# 写入文件
f.write(message1+message2)
# 关闭文件
f.close()

# 运行完自动在网页中显示
webbrowser.open(GEN_HTML, new=1)



