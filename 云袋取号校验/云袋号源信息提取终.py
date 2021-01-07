import requests,json
import pymysql
from io import BytesIO
from pyzbar import pyzbar
from PIL import Image
import time
from 云袋取号校验 import oss阿里云数据检测

class Yundai:
    def __init__(self):
        pass

    def get_data(self):
        #访问云贷取号接口，将信息拿出,将接口中的json字符串信息进行反序列化
        url = 'http://api.goluodi.com/shunwang/gettask?SenceId=223.196.75.106=&areacode&business_type=2'
        response = requests.get(url=url)
        res = response.json()
        obj = res['data']
        # print(obj)
        appid_list = []
        gh_id_list = []
        qrcode_url_list = []
        nick_name_list = []
        priority_list = []
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

        return obj,appid_list,gh_id_list,qrcode_url_list,nick_name_list,data_appids,now_time

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
        # print(authorizer_qrcode_link_list)
        return authorizer_qrcode_link_list

    def yundai(self,authorizer_qrcode_link_list,appid_list,gh_id_list,qrcode_url_list,nick_name_list,data_appids,now_time):
        # 建立数据库连接
        conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='qwe123',
            db='yundai',
            charset='utf8'
            # host='10.8.91.153',
            # port=3306,
            # user='tiancanrw',
            # password='tiancan#168',
            # db='aquarius_ads',
            # charset='utf8'
        )
        # 获取游标
        cursor = conn.cursor()
        # sql = """alter table `ads_resource` AUTO_INCREMENT=6;"""
        # cursor.execute(sql)
        # 查出pid=2的config字段列的所有数据
        sql = """select config from ads_resource WHERE pid=2 AND NOT LOCATE ('云袋',title)"""
        rows = cursor.execute(sql)
        if rows > 0:
            config_appid_dics = {'appid': []}
            config_link_dics = {}
            config_tups = cursor.fetchall()
            # print(config_tups)#打印出config字段的所有元组数据
            for config_tup in config_tups:
                # print(json.loads(config_tup[0]),type(json.loads(config_tup[0])))
                config_dic = json.loads(config_tup[0])
                appid = config_dic['authorizer_appid']
                config_appid_dics['appid'].append(appid)  # 将appid的值拿出来添加到列表中

            # 从数据库中拿出来的config数据去跟号源信息比对
            for config_tup in config_tups:
                # 将数据库中的appid信息与号源中的appid进行比对判断
                if json.loads(config_tup[0])['authorizer_appid'] in data_appids:
                    # 如果数据库中的appid在拿到的号源信息中，先对state信息进行比对修改
                    sql = """select state from ads_resource WHERE title='%s'""" % json.loads(config_tup[0])[
                        'authorizer_nickname']
                    cursor.execute(sql)
                    state = cursor.fetchone()
                    if state[0] == 1:
                        pass
                    else:
                        sql = """update `ads_resource` set state = 1 where title = '%s'""" % json.loads(config_tup[0])[
                            'authorizer_nickname']
                        cursor.execute(sql)
                        conn.commit()
                    # 遍历号源信息中的appid，找出与本次循环一致得appid，对url链接进行比对
                    for data_appid in data_appids:
                        if data_appid == json.loads(config_tup[0])['authorizer_appid']:
                            i = data_appids.index(data_appid)
                            # 对微信链接进行修改
                            if json.loads(config_tup[0])['authorizer_qrcode_link'] == authorizer_qrcode_link_list[i]:
                                print('微信链接一致,此次判断的商家为%s' % nick_name_list[i])
                                print(' ')
                                break
                            else:
                                sql = """update ads_resource set config = json_set(config,"$.authorizer_qrcode_link",'%s') where title = '%s';""" % (
                                    authorizer_qrcode_link_list[i], json.loads(config_tup[0])['authorizer_nickname'])
                                cursor.execute(sql)
                                conn.commit()
                                # 将此处的机器人hook地址替换为你创建的机器人地址即可
                                webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=61b95963-c5ce-4777-9f82-75823d29b301"
                                text_push_content = """%s的url链接发生了变化，已修改(测试消息)""" % json.loads(config_tup[0])[
                                    'authorizer_nickname']

                                text_data = {
                                    "msgtype": "text",
                                    "text": {
                                        "content": text_push_content,
                                        "mentioned_list": ["xuejian"]
                                    }
                                }

                                def post_data(webhook_url, text_data):
                                    # 注意：data发送时，一定要是json格式，另外，字符编码需要是utf-8
                                    postdata = str(json.dumps(text_data)).encode('utf-8')
                                    r = requests.post(webhook_url, data=postdata)
                                    # print(r.text)
                                    print('消息已通知')
                                post_data(webhook_url, text_data)
                                oss阿里云数据检测.run(gh_id_list,i,authorizer_qrcode_link_list)
                                break
                        else:
                            # pass
                            print('此次判断的APPID不一致')
                else:
                    print('号源信息中没有查询到%s的相关数据' % json.loads(config_tup[0])['authorizer_nickname'])
                    sql = """update `ads_resource` set state = 2 where title = '%s'""" % json.loads(config_tup[0])[
                        'authorizer_nickname']
                    cursor.execute(sql)
                    conn.commit()

            for data_appid in data_appids:
                i = data_appids.index(data_appid)
                if data_appid not in config_appid_dics['appid']:
                    # 如果不存在，进行信息添加
                    sql = """INSERT INTO `ads_resource`(`pid`, `title`, `form_name`, `classify`, `config`, `desc`, `state`, `creater_username`, `creater_realname`, `is_audit`, `audit_username`, `audit_realname`, `audited_at`, `created_at`, `updated_at`, `deleted_at`) VALUES (2, '%s', 'IMAGE_QRCODE_WECHAT', 1, '{\"width\": 150, \"height\": 150, \"authorizer_appid\": \"%s\", \"authorizer_nickname\": \"%s\", \"authorizer_username\": \"%s\", \"authorizer_principal\": \"云袋有限公司\", \"authomysql> rcode_str\": \"\", \"authorizer_qrcode_link\": \"%s\", \"authorizer_qrcode_ticket\": \"\", \"authorizer_qrcode_img_url\": \"%s\"}', NULL, 1, 'sysadmin', 'sysadmin', 1, 'sysadmin', 'sysadmin', '%s' , '%s' , NULL , NULL);""" % (
                        nick_name_list[i], appid_list[i], nick_name_list[i], gh_id_list[i], authorizer_qrcode_link_list[i],
                        qrcode_url_list[i], now_time, now_time)
                    print('此次插入的数据为%s' % nick_name_list[i])
                    cursor.execute(sql)
                    conn.commit()
        else:
            for data_appid in data_appids:
                i = data_appids.index(data_appid)
                sql = """INSERT INTO `ads_resource`(`pid`, `title`, `form_name`, `classify`, `config`, `desc`, `state`, `creater_username`, `creater_realname`, `is_audit`, `audit_username`, `audit_realname`, `audited_at`, `created_at`, `updated_at`, `deleted_at`) VALUES (2, '%s', 'IMAGE_QRCODE_WECHAT', 1, '{\"width\": 150, \"height\": 150, \"authorizer_appid\": \"%s\", \"authorizer_nickname\": \"%s\", \"authorizer_username\": \"%s\", \"authorizer_principal\": \"云袋有限公司\", \"authomysql> rcode_str\": \"\", \"authorizer_qrcode_link\": \"%s\", \"authorizer_qrcode_ticket\": \"\", \"authorizer_qrcode_img_url\": \"%s\"}', NULL, 1, 'sysadmin', 'sysadmin', 1, 'sysadmin', 'sysadmin', '%s' , '%s' , NULL , NULL);""" % (
                    nick_name_list[i], appid_list[i], nick_name_list[i], gh_id_list[i], authorizer_qrcode_link_list[i],
                    qrcode_url_list[i], now_time, now_time)
                print('此次插入的数据为%s' % nick_name_list[i])
                cursor.execute(sql)
                conn.commit()
        return conn,cursor

    def close(self,conn,cursor):
        # 关闭游标
        cursor.close()
        # 关闭链接
        conn.close()

    def run(self):
        obj, appid_list, gh_id_list, qrcode_url_list, nick_name_list, data_appids, now_time = self.get_data()
        authorizer_qrcode_link_list = self.get_imgurl(obj, qrcode_url_list)
        conn,cursor = self.yundai(authorizer_qrcode_link_list, appid_list, gh_id_list, qrcode_url_list, nick_name_list, data_appids,
                 now_time)
        self.close(conn,cursor)

if __name__ == '__main__':
    a = Yundai()
    a.run()
