# --*-- coding: utf-8 --*--
# @Author: Fangyu
# @Email:fangyu@tiancan.tech
# @Time: 2020/11/23 9:08
# @File: data.py
import requests,json
import pymysql
from io import BytesIO
from pyzbar import pyzbar
from PIL import Image
import time
from 准粉吧 import ali_oss_data_inspect,up_downline_msg,update_msg
import hashlib

class Zhunfenba:
    def __init__(self):
        pass

    def get_data(self):
        #访问云贷取号接口，将信息拿出,将接口中的json字符串信息进行反序列化
        url = 'https://search-api.shenghuoq.com/dmp-search-api/v4/ad/noauth'
        headers = {
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
            'Content-Type': "application/json"
        }
        body = {
            "appNo": "527017ac0142bb93",
            "openId": "oVmEd1HfcTS7TDQIo7-Rwf5ytt8U",
            "facilityId": "95234gd27",
            "userAgent": "Mozilla/5.0 (Linux; Android 7.0; Mi-4c Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043632 Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN miniProgram",
            "sex": 0,
            "nickname": "1234",
            "creativityType": 1,
            "redirect": ""
        }
        response = requests.post(url=url, data=json.dumps(body), headers=headers)
        res = response.json()
        obj = res['result']['data']
        wxid_list = []
        ghid_list = []
        qrPicUrl_list = []
        nickname_list = []
        #将wxid值取出
        data_wxids = []
        for data in obj:
            data_wxids.append(data['wxId'])
        # 将接口中的信息取出备用
        for i in range(len(obj)):
            now_time = time.strftime("%Y-%m-%d %X")
            wxid_list.append(obj[i]['wxId'])
            ghid_list.append(obj[i]['ghId'])
            nickname_list.append(obj[i]['nickName'])

        return obj,wxid_list,ghid_list,qrPicUrl_list,nickname_list,data_wxids,now_time

    def get_imgurl(self,obj,qrPicUrl_list):
        # 解析二维码对应的链接并添加到所需列表中
        authorizer_qrcode_img_url_list = []
        for i in range(len(obj)):
            qrPicUrl_list.append(obj[i]['qrPicUrl'])

        def get_ewm(url):
            rq_img = requests.get(url).content
            img = Image.open(BytesIO(rq_img))
            # img.show()  # 显示图片，测试用
            txt_list = pyzbar.decode(img)
            for txt in txt_list:
                barcodeData = txt.data.decode("utf-8")
                authorizer_qrcode_img_url_list.append(barcodeData)

        for url in qrPicUrl_list:
            get_ewm(url)
        return authorizer_qrcode_img_url_list


    def md5Encode(self,str):
        # 创建md5对象
        m = hashlib.md5()
        m.update(str)  # 传入需要加密的字符串进行MD5加密
        return m.hexdigest()  # 获取到经过MD5加密的字符串并返回
    def get_mad(self,gh_id_list,i):
        bb = self.md5Encode(gh_id_list[i].encode('utf-8')) # 必须先进行转码，否则会报错
        return bb

    def zhunfenba(self,authorizer_qrcode_img_url_list,wxid_list,ghid_list,qrPicUrl_list,nickname_list,data_wxids,now_time):
        # 建立数据库连接
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
        sql = """select config from ads_resource WHERE pid=3 """
        rows = cursor.execute(sql)
        if rows > 0:
            config_appid_dics = {'appid': []}
            config_tups = cursor.fetchall()
            # 从数据库中拿出来的config数据去跟号源信息比对
            for config_tup in config_tups:
                config_dic = json.loads(config_tup[0])
                appid = config_dic['authorizer_appid']
                config_appid_dics['appid'].append(appid)  # 将appid的值拿出来添加到列表中
                # 如果数据库中的appid在拿到的号源信息中，先对state信息进行比对修改
                sql = """select state from ads_resource WHERE title='%s'""" % ('准粉吧'+json.loads(config_tup[0])['authorizer_nickname'])
                cursor.execute(sql)
                state = cursor.fetchone()
                # 将数据库中的appid信息与号源中的appid进行比对判断
                if json.loads(config_tup[0])['authorizer_appid'] in data_wxids:
                    if state[0] == 1:
                        pass
                    else:
                        sql = """update `ads_resource` set state = 1 where title = '%s'""" % json.loads(config_tup[0])[
                            'authorizer_nickname']
                        cursor.execute(sql)
                        conn.commit()
                        authorizer_nickname = json.loads(config_tup[0])
                        up_downline_msg.run2(authorizer_nickname)
                    # 遍历号源信息中的appid，找出与本次循环一致得appid，对url链接进行比对
                    for data_wxid in data_wxids:
                        if data_wxid == json.loads(config_tup[0])['authorizer_appid']:
                            i = data_wxids.index(data_wxid)
                            # 对微信链接进行修改
                            if json.loads(config_tup[0])['authorizer_qrcode_link'] == authorizer_qrcode_img_url_list[i]:
                                print('微信链接一致,此次判断的商家为%s' % nickname_list[i])
                                print(' ')
                                break
                            else:
                                sql = """update ads_resource set config = json_set(config,"$.authorizer_qrcode_img_url",'%s') where title = '%s';""" % (
                                    authorizer_qrcode_img_url_list[i], json.loads(config_tup[0])['authorizer_nickname'])
                                cursor.execute(sql)
                                conn.commit()
                                # 自动发送微信消息提醒
                                update_msg.run(nickname_list,i)
                                ali_oss_data_inspect.run(ghid_list, i, authorizer_qrcode_img_url_list)
                                break
                        else:
                            pass
                            # print('此次判断的APPID不一致')

                    sql = """update `zhunfenba_extra` set `check_times`=0 WHERE appid='%s'"""%(json.loads(config_tup[0])['authorizer_appid'])
                    cursor.execute(sql)
                    conn.commit()
                else:
                    #如果数据库中的信息不在号源信息中，并且state数值等于1，先去比较check_times的数值，如果check_times
                    #小于等于15，加1，大于15，将state数值改为2
                    if state[0] == 1:
                        sql = """select `check_times` from `zhunfenba_extra` WHERE appid='%s'""" % (
                        json.loads(config_tup[0])['authorizer_appid'])
                        cursor.execute(sql)
                        check_times = cursor.fetchone()[0]
                        if check_times <= 15:
                            sql = """update `zhunfenba_extra` set `check_times`='%s' WHERE appid='%s'""" % (
                            check_times + 1, json.loads(config_tup[0])['authorizer_appid'])
                            cursor.execute(sql)
                            conn.commit()
                            print('号源信息中没有查询到%s的相关数据' % json.loads(config_tup[0])['authorizer_nickname'])
                        else:
                            sql = """update `ads_resource` set state = 2 where title = '%s'""" % json.loads(config_tup[0])[
                                'authorizer_nickname']
                            cursor.execute(sql)
                            conn.commit()
                            print('号源信息中没有查询到%s的相关数据' % json.loads(config_tup[0])['authorizer_nickname'])
                            authorizer_nickname = json.loads(config_tup[0])
                            up_downline_msg.run1(authorizer_nickname)
                    else:
                        #如果数据库中的信息不在号源信息中，并且state数值等于2，那没事了
                        print('号源信息中没有查询到%s的相关数据' % json.loads(config_tup[0])['authorizer_nickname'])
            for data_wxid in data_wxids:
                i = data_wxids.index(data_wxid)
                bb = self.get_mad(ghid_list, i)
                if data_wxid not in config_appid_dics['appid']:
                    # 如果不存在，进行信息添加
                    sql = """INSERT INTO `ads_resource`(`pid`, `title`, `form_name`, `classify`, `config`, `state`, `creater_username`, `creater_realname`, `is_audit`, `audit_username`, `audit_realname`, `audited_at`, `created_at`, `updated_at`, `deleted_at`) VALUES (3, '%s', 'IMAGE_QRCODE_WECHAT', 1, '{\"width\": 150, \"height\": 150, \"authorizer_appid\": \"%s\", \"authorizer_nickname\": \"%s\", \"authorizer_username\": \"%s\", \"authorizer_principal\": \"准粉吧\", \"authorizer_qrcode_str\": \"\", \"authorizer_qrcode_link\": \"%s\", \"authorizer_qrcode_ticket\": \"\", \"authorizer_qrcode_img_url\": \"%s\"}', 1, 'sysadmin', 'sysadmin', 1, 'sysadmin', 'sysadmin', '%s' , '%s' , NULL , NULL);""" % (
                        '准粉吧'+nickname_list[i], wxid_list[i], nickname_list[i], ghid_list[i],
                        authorizer_qrcode_img_url_list[i], 'http://res.tiancan.online'+bb+'.png', now_time, now_time)
                    print('此次插入的数据为%s' % nickname_list[i])
                    print(' ')
                    cursor.execute(sql)
                    conn.commit()
                    sql = """INSERT INTO `zhunfenba_extra`(`appid`, `check_times`) VALUES ('%s',0)""" % (data_wxid)
                    cursor.execute(sql)
                    conn.commit()
                    ali_oss_data_inspect.run(ghid_list, i, authorizer_qrcode_img_url_list)
                    #自动发送微信消息提醒
                    update_msg.run(nickname_list,i)
        else:
            for data_wxid in data_wxids:
                i = data_wxids.index(data_wxid)
                bb = self.get_mad(ghid_list, i)
                sql = """INSERT INTO `ads_resource`(`pid`, `title`, `form_name`, `classify`, `config`, `state`, `creater_username`, `creater_realname`, `is_audit`, `audit_username`, `audit_realname`, `audited_at`, `created_at`, `updated_at`, `deleted_at`) VALUES (3, '%s', 'IMAGE_QRCODE_WECHAT', 1, '{\"width\": 150, \"height\": 150, \"authorizer_appid\": \"%s\", \"authorizer_nickname\": \"%s\", \"authorizer_username\": \"%s\", \"authorizer_principal\": \"准粉吧\", \"authorizer_qrcode_str\": \"\", \"authorizer_qrcode_link\": \"%s\", \"authorizer_qrcode_ticket\": \"\", \"authorizer_qrcode_img_url\": \"%s\"}', 1, 'sysadmin', 'sysadmin', 1, 'sysadmin', 'sysadmin', '%s' , '%s' , NULL , NULL);""" % (
                    '准粉吧' +nickname_list[i], wxid_list[i], nickname_list[i], ghid_list[i], authorizer_qrcode_img_url_list[i],
                    'http://res.tiancan.online' + bb + '.png', now_time, now_time)
                print('此次插入的数据为%s' % nickname_list[i])
                print(' ')
                cursor.execute(sql)
                conn.commit()
                sql = """INSERT INTO `zhunfenba_extra`(`appid`, `check_times`) VALUES ('%s',0)"""%(data_wxid)
                cursor.execute(sql)
                conn.commit()
                ali_oss_data_inspect.run(ghid_list, i, authorizer_qrcode_img_url_list)
                # 自动发送微信消息提醒
                update_msg.run(nickname_list, i)
        return conn,cursor

    def close(self,conn,cursor):
        # 关闭游标
        cursor.close()
        # 关闭链接
        conn.close()

    def run(self):
        obj, wxid_list, ghid_list, qrPicUrl_list, nickname_list, data_wxids, now_time = self.get_data()
        authorizer_qrcode_img_url_list = self.get_imgurl(obj, qrPicUrl_list)
        conn,cursor = self.zhunfenba(authorizer_qrcode_img_url_list, wxid_list, ghid_list, qrPicUrl_list, nickname_list, data_wxids,
                 now_time)
        self.close(conn,cursor)

if __name__ == '__main__':
    a = Zhunfenba()
    a.run()
