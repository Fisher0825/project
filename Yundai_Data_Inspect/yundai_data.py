import requests,json
from io import BytesIO
from pyzbar import pyzbar
from PIL import Image
import time
from Yundai_Data_Inspect import ali_oss_data_inspect,up_downline_msg,update_msg,settings
import hashlib

class Yundai:
    def __init__(self):
        pass

    def get_data(self, addr):
        #访问云贷取号接口，将信息拿出,将接口中的json字符串信息进行反序列化
        url = 'http://api.goluodi.com/%s/gettask?SenceId=223.196.75.106=&areacode&business_type=2'%addr
        response = requests.get(url=url)
        res = response.json()
        return res
    def make_data(self,obj):
        appid_list = []
        gh_id_list = []
        qrcode_url_list = []
        nick_name_list = []
        #将appid值取出
        data_appids = []
        for data in obj:
            data_appids.append(data['appid'])
        # 将接口中的信息取出备用
        for i in range(len(obj)):
            now_time = time.strftime("%Y-%m-%d %X")
            appid_list.append(obj[i]['appid'])
            gh_id_list.append(obj[i]['gh_id'])
            nick_name_list.append(obj[i]['nick_name'])

        return appid_list,gh_id_list,qrcode_url_list,nick_name_list,data_appids,now_time

    def get_imgurl(self,obj,qrcode_url_list):
        # 解析二维码对应的链接并添加到所需列表中
        authorizer_qrcode_link_list = []
        for i in range(len(obj)):
            qrcode_url_list.append(obj[i]['qrcode_url'])

        def get_ewm(self,url):
            rq_img = requests.get(url).content
            img = Image.open(BytesIO(rq_img))
            # img.show()  # 显示图片，测试用
            txt_list = pyzbar.decode(img)
            for txt in txt_list:
                barcodeData = txt.data.decode("utf-8")
                authorizer_qrcode_link_list.append(barcodeData)

        for url in qrcode_url_list:
            get_ewm(self,url)
        return authorizer_qrcode_link_list

    def md5Encode(self,str):
        # 创建md5对象
        m = hashlib.md5()
        m.update(str)  # 传入需要加密的字符串进行MD5加密
        return m.hexdigest()  # 获取到经过MD5加密的字符串并返回
    def get_mad(self,gh_id_list,i):
        bb = self.md5Encode(gh_id_list[i].encode('utf-8')) # 必须先进行转码，否则会报错
        return bb

    def yundai(self,authorizer_qrcode_link_list,appid_list,gh_id_list,nick_name_list,data_appids,now_time):
        conn, cursor = settings.Conn()
        sql = """select config from ads_resource WHERE pid=2 AND NOT LOCATE ('云袋',title)"""
        rows = cursor.execute(sql)
        if rows > 0:
            config_appid_dics = {'appid': []}
            config_tups = cursor.fetchall()
            # print(config_tups)#打印出config字段的所有元组数据，测试用
            for config_tup in config_tups:
                # print(json.loads(config_tup[0]),type(json.loads(config_tup[0])))
                config_dic = json.loads(config_tup[0])
                appid = config_dic['authorizer_appid']
                config_appid_dics['appid'].append(appid)  # 将appid的值拿出来添加到列表中
            # 从数据库中拿出来的config数据去跟号源信息比对
            for config_tup in config_tups:
                # print(config_tup[0])
                # 如果数据库中的appid在拿到的号源信息中，先对state信息进行比对修改
                sql = """select state from ads_resource WHERE json_extract(config,"$.authorizer_appid")='%s' AND pid=2""" % json.loads(config_tup[0])['authorizer_appid']
                cursor.execute(sql)
                state = cursor.fetchone()
                # 将数据库中的appid信息与号源中的appid进行比对判断
                if json.loads(config_tup[0])['authorizer_appid'] in data_appids:
                    if state[0] == 1:
                        pass
                    else:
                        sql = """update `ads_resource` set state = 1 where json_extract(config,"$.authorizer_appid")='%s' AND pid=2""" % json.loads(config_tup[0])['authorizer_appid']
                        cursor.execute(sql)
                        conn.commit()
                        authorizer_nickname = json.loads(config_tup[0])
                        up_downline_msg.run2(authorizer_nickname)
                    # 遍历号源信息中的appid，找出与本次循环一致得appid，对url链接进行比对
                    for data_appid in data_appids:
                        if data_appid == json.loads(config_tup[0])['authorizer_appid']:
                            i = data_appids.index(data_appid)
                            # 对微信链接进行修改
                            if json.loads(config_tup[0])['authorizer_qrcode_link'] == authorizer_qrcode_link_list[i]:
                                print('\n微信链接一致,此次判断的商家为%s\n' % nick_name_list[i])
                                break
                            else:
                                sql = """update ads_resource set config = json_set(config,"$.authorizer_qrcode_link",'%s') where json_extract(config,"$.authorizer_appid")='%s' AND pid=2;""" % (
                                    authorizer_qrcode_link_list[i], json.loads(config_tup[0])['authorizer_appid'])
                                cursor.execute(sql)
                                conn.commit()
                                # 自动发送微信消息提醒
                                update_msg.run(nick_name_list,i)
                                ali_oss_data_inspect.run(gh_id_list, i, authorizer_qrcode_link_list)
                                break
                        else:
                            pass
                            # print('此次判断的APPID不一致')
                else:
                    if state[0] == 1:
                        sql = """update `ads_resource` set state = 2 where json_extract(config,"$.authorizer_appid")='%s' AND pid=2""" % json.loads(config_tup[0])['authorizer_appid']
                        cursor.execute(sql)
                        conn.commit()
                        print('号源信息中没有查询到%s的相关数据' % json.loads(config_tup[0])['authorizer_nickname'])
                        authorizer_nickname = json.loads(config_tup[0])
                        up_downline_msg.run1(authorizer_nickname)
                    else:
                        print('号源信息中没有查询到%s的相关数据' % json.loads(config_tup[0])['authorizer_nickname'])
            for data_appid in data_appids:
                i = data_appids.index(data_appid)
                bb = self.get_mad(gh_id_list,i)
                if data_appid not in config_appid_dics['appid']:
                    # 如果不存在，进行信息添加
                    sql = """INSERT INTO `ads_resource`(`pid`, `title`, `form_name`, `classify`, `config`, `desc`, `state`, `creater_username`, `creater_realname`, `is_audit`, `audit_username`, `audit_realname`, `audited_at`, `created_at`, `updated_at`, `deleted_at`) VALUES (2, '%s', 'IMAGE_QRCODE_WECHAT', 1, '{\"width\": 150, \"height\": 150, \"authorizer_appid\": \"%s\", \"authorizer_nickname\": \"%s\", \"authorizer_username\": \"%s\", \"authorizer_principal\": \"云袋有限公司\", \"authomysql> rcode_str\": \"\", \"authorizer_qrcode_link\": \"%s\", \"authorizer_qrcode_ticket\": \"\", \"authorizer_qrcode_img_url\": \"%s\"}', NULL, 1, 'sysadmin', 'sysadmin', 1, 'sysadmin', 'sysadmin', '%s' , '%s' , NULL , NULL);""" % (
                        nick_name_list[i], appid_list[i], nick_name_list[i], gh_id_list[i], authorizer_qrcode_link_list[i],
                        'http://res.tiancan.online/'+bb+'.png', now_time, now_time)
                    print('此次插入的数据为%s\n' % nick_name_list[i])
                    cursor.execute(sql)
                    conn.commit()
                    ali_oss_data_inspect.run(gh_id_list, i, authorizer_qrcode_link_list)
                    #自动发送微信消息提醒
                    update_msg.run(nick_name_list,i)
        else:
            for data_appid in data_appids:
                i = data_appids.index(data_appid)
                bb = self.get_mad(gh_id_list, i)
                sql = """INSERT INTO `ads_resource`(`pid`, `title`, `form_name`, `classify`, `config`, `desc`, `state`, `creater_username`, `creater_realname`, `is_audit`, `audit_username`, `audit_realname`, `audited_at`, `created_at`, `updated_at`, `deleted_at`) VALUES (2, '%s', 'IMAGE_QRCODE_WECHAT', 1, '{\"width\": 150, \"height\": 150, \"authorizer_appid\": \"%s\", \"authorizer_nickname\": \"%s\", \"authorizer_username\": \"%s\", \"authorizer_principal\": \"云袋有限公司\", \"authomysql> rcode_str\": \"\", \"authorizer_qrcode_link\": \"%s\", \"authorizer_qrcode_ticket\": \"\", \"authorizer_qrcode_img_url\": \"%s\"}', NULL, 1, 'sysadmin', 'sysadmin', 1, 'sysadmin', 'sysadmin', '%s' , '%s' , NULL , NULL);""" % (
                    nick_name_list[i], appid_list[i], nick_name_list[i], gh_id_list[i], authorizer_qrcode_link_list[i],
                    'http://res.tiancan.online/' + bb + '.png', now_time, now_time)
                print('此次插入的数据为%s\n' % nick_name_list[i])
                cursor.execute(sql)
                conn.commit()
                ali_oss_data_inspect.run(gh_id_list, i, authorizer_qrcode_link_list)
                # 自动发送微信消息提醒
                update_msg.run(nick_name_list, i)
        return conn,cursor

    def close(self,conn,cursor):
        # 关闭游标
        cursor.close()
        # 关闭链接
        conn.close()

    def run(self):
        responses = {'errcode': 0, 'data': []}
        for addr in ['shunwang', 'lianwo']:
            res = self.get_data(addr)
            res_str = str(res)
            # print(res_str)
            if 'data' in res_str:
                for Data in res['data']:
                    responses['data'].append(Data)
        # print('responses:',responses)
        obj = responses['data']
        if obj:
            appid_list, gh_id_list, qrcode_url_list, nick_name_list, data_appids, now_time = self.make_data(obj)
            authorizer_qrcode_link_list = self.get_imgurl(obj, qrcode_url_list)
            conn,cursor = self.yundai(authorizer_qrcode_link_list, appid_list, gh_id_list, nick_name_list, data_appids,
                     now_time)
            self.close(conn,cursor)
        else:
            conn, cursor = settings.Conn()
            sql = """update `ads_resource` set state = 2 where pid=2 AND id != 2 AND id != 67"""
            cursor.execute(sql)
            conn.commit()
            self.close(conn,cursor)
            print('号源中没有信息，已将所有state信息修改')
if __name__ == '__main__':
    try:
        a = Yundai()
        a.run()
    except:
        a = Yundai()
        a.run()

