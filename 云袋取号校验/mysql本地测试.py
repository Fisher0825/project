import pymysql
import requests
from io import BytesIO
from pyzbar import pyzbar
from PIL import Image, ImageEnhance


url = 'http://api.goluodi.com/shunwang/gettask?SenceId=223.196.75.106=&areacode&business_type=2'
#先从接口中拿到所有appid的信息
response = requests.get(url=url)
page_text = response.text
# with open('test.txt','w',encoding='utf-8') as fp:
#     fp.write(page_text)
res = response.json()

appid_list = []
gh_id_list = []
qrcode_url_list = []
nick_name_list = []
priority_list = []
obj = res['data']
for i in range(len(obj)):
    appid_list.append(obj[i]['appid'])
    gh_id_list.append(obj[i]['gh_id'])
    qrcode_url_list.append(obj[i]['qrcode_url'])
    nick_name_list.append(obj[i]['nick_name'])
    priority_list.append(obj[i]['priority'])
# print(json.dumps(qrcode_url_list)) #将拿出来的字符串进行反序列化，变成json字符串方便存入数据库
print(qrcode_url_list)

#解析二维码并添加到所需列表中
authorizer_qrcode_link = []
def get_ewm(img_adds):
    rq_img = requests.get(img_adds).content
    img = Image.open(BytesIO(rq_img))
    # img.show()  # 显示图片，测试用
    txt_list = pyzbar.decode(img)
    for txt in txt_list:
        barcodeData = txt.data.decode("utf-8")
        authorizer_qrcode_link.append(barcodeData)
for url in qrcode_url_list:
    get_ewm(url)

# 建立数据库连接
conn=pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='qwe123',
    db='weifensi',
    charset='utf8'
)

#获取游标
cursor = conn.cursor()
sql = """select * from fans;"""

# #创建数据库
# sql = """CREATE DATABASE IF NOT EXISTS yundai DEFAULT CHARSET utf8 COLLATE utf8_general_ci;"""
# cursor.execute(sql)
# #创建表
# sql = """CREATE TABLE IF NOT EXISTS ads_resource (id int(11) NOT NULL AUTO_INCREMENT,)"""
#
# #执行sql语句
sql = """insert into ads_resource(pid,title,form_name,classify,config,desc,state,creater_username,creater_realname,is_audit,audit_username,audit_realname,audited_at,created_at,updated_at,deleted_at) VALUES (2,s%,`IMAGE_QRCODE_WECHAT`,1,{"width":150,"height": 150,"authorizer_appid":s%,"authorizer_nickname":s%,"authorizer_username":s%,"authorizer_principal":s%,"authomysql> rcode_str":"","authorizer_qrcode_link":s%,"authorizer_qrcode_ticket":"","authorizer_qrcode_img_url":s%,},NULL,1,sysadmin,sysadmin,1,sysadmin,sysadmin,s%,s%,NULL ,NULL)"""

rows = cursor.execute(sql)
print(cursor.fetchall())
#关闭游标
cursor.close()
#关闭链接
conn.close()
# 判断是否连接成功
if rows >= 0:
    print('连接数据库成功')
else:
    print('连接数据库失败')
