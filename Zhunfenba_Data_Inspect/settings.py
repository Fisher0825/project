# --*-- coding: utf-8 --*--
# @Author: Fangyu
# @Email:fangyu@tiancan.tech
# @Time: 2020/11/24 13:48
# @File: seetings.py
import pymysql
import oss2

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

#阿里云oss服务的数据链接在这里修改
def aliyun_oss():
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    auth = oss2.Auth('LTAI4G5VUWNavHFqPJucReLo', '3BRXG5pK806NTlrBL0UHGcuC8SIZEJ')
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth, 'http://oss-cn-hongkong.aliyuncs.com', 'resjinguidnacom')
    return bucket