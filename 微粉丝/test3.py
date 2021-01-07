import requests
import random
from hashlib import md5
from lxml import etree
import time
import pandas as pd
from sqlalchemy import create_engine
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler
import sys


class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()
def verification_code_rec(imgpath,imgtype):
    chaojiying = Chaojiying_Client('fangyu', 'fangyu1996825', '907185')#用户中心>>软件ID 生成一个替换 96001
    im = open(imgpath, 'rb').read()#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    return chaojiying.PostPic(im, imgtype)#1004 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'Referer': 'https://buss.weifenshi.cn/',
            'Host': 'buss.weifenshi.cn'
        }
# login_url = 'https://buss.weifenshi.cn'
# page_text = requests.get(url=login_url,headers=headers).text
# tree = etree.HTML(page_text)
# img_path = 'https://buss.weifenshi.cn' + tree.xpath('//*[@id="captchaImg"]/@src')[0]
# img_data = requests.get(url=img_path, headers=headers).content  # 请求到了图片数据
# with open('./code.jpg', 'wb') as fp:
#     fp.write(img_data)
url = 'https://buss.weifenshi.cn/index.php/index/verify'
response = requests.get(url=url, headers=headers,verify=False)
with open('code.jpg', 'wb') as f:
    f.write(response.content)
code_result = verification_code_rec('./code.jpg', 1004)

#获取callback:jQuery后面的随机参数并且登录
code_source = '0123456789'
ran_num = ''
for i in range(16):
    # 随机选择一个字符
    s = code_source[random.randrange(0, len(code_source) - 1)]
    ran_num += s
timestamp = str(int(time.time() * 1000))
url = 'https://buss.weifenshi.cn/index.php/index/check_login?callback=jQuery1910{}_{}&username={}&password={}&verify_code={}&_={}'.format(ran_num, timestamp, 'tckj', 'tckj008008', code_result, timestamp)
weifensiSession = requests.Session()
response = weifensiSession.get(url=url, headers=headers, verify=False)
cookie=''
for k,v in response.cookies.iteritems():
    cookie+= k+'='+v+";"
    cookie=cookie[:-1]
    print(cookie)

class Data:

    def __init__(self, ip, port, username, password, database, table_name):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.table_name = table_name

    def spider_data(self):
        """
        爬数据
        :return:
        """
        url = 'https://buss.weifenshi.cn/index.php/buss/summary'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            "cookie": cookie,
            'Referer': 'https://buss.weifenshi.cn/',
            'Host': 'buss.weifenshi.cn'
        }
        sess = requests.Session()
        page_text = sess.get(url=url, headers=headers).text
        data_dict = {}
        tree = etree.HTML(page_text)
        r = tree.xpath('//*[@id="main_1"]/div[1]/div/dl[1]/dd/text()')
        earning = r[0] if r else None
        day_fans = tree.xpath('//*[@id="main_1"]/div[1]/div/dl[2]/dd/text()')[0]
        month_fans = tree.xpath('//*[@id="main_1"]/div[1]/div/dl[3]/dd/text()')[0]
        total_fans = tree.xpath('//*[@id="main_1"]/div[1]/div/dl[4]/dd/text()')[0]
        time_stamp = time.strftime("%Y-%m-%d %X")
        data_dict["today_earnings"] = earning
        data_dict["today_fans"] = day_fans
        data_dict["month_fans"] = month_fans
        data_dict["total_fans"] = total_fans
        data_dict["time_stamp"] = time_stamp
        data_df = pd.DataFrame(data_dict, index=[0])
        return data_df

    def insert_data(self, data):
        """
        ip:10.8.91.153
        port:3306
        username：reptile
        password：3mF5pAXEdoCZJ49c

        table_name:Data
        :return:

        create table fans(
            id  int(100) primary key not null auto_increment,
            today_earnings float,
            today_fans int,
            month_fans int,
            total_fans int,
            time_stamp datetime
        );
        """
        engine = create_engine(f"mysql+pymysql://{self.username}:{self.password}@{self.ip}:{self.port}/{self.database}")
        try:
            data.to_sql(name=f"{self.table_name}", con=engine, if_exists="append", index=False)
            print("插入数据成功")
        except:
            print("插入数据失败")


def main(ip, port, username, password, database, table_name):
    class_data = Data(ip, port, username, password, database, table_name)
    data = class_data.spider_data()
    class_data.insert_data(data)

executers = {
    "default": ThreadPoolExecutor(2)
}


def run1(ip, port, username, password, database, table_name):
    scheduler = BlockingScheduler(executers=executers)
    scheduler.add_job(main, 'interval', seconds=5,
                      kwargs={"ip": ip, "port": port, "username": username, "password": password, "database": database,
                              "table_name": table_name})
    scheduler.start()

params = sys.argv[1:]

if __name__ == '__main__':
    run1('127.0.0.1','3306','root','qwe123','weifensi','fans')
    # 运行代码时：python spider.py ip port username password database table_name