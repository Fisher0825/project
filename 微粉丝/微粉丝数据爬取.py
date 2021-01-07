from selenium import webdriver
from PIL import Image#进行截图裁剪
import requests
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
def transform_code_img(imgpath,imgtype):
    chaojiying = Chaojiying_Client('fangyu', 'fangyu1996825', '907185')#用户中心>>软件ID 生成一个替换 96001
    im = open(imgpath, 'rb').read()   #本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    return chaojiying.PostPic(im, imgtype)   #1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()

url = 'https://buss.weifenshi.cn'
bro = webdriver.Chrome(executable_path='./chromedriver')
bro.get(url)

username = bro.find_element_by_name('username')   #获取账户框
time.sleep(2)
username.send_keys('tckj')

password = bro.find_element_by_name('password')   #获取密码框
time.sleep(2)
password.send_keys(('tckj008008'))
ver_code = bro.find_element_by_name('verify_code')

bro.save_screenshot('./main.png')
code_img = bro.find_element_by_xpath('//*[@id="captchaImg"]')
location = code_img.location
size = code_img.size
rangle = (int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height']))

#基于Image类提供的工具进行裁剪
i = Image.open('./main.png')
frame = i.crop(rangle)
frame.save('./code.png')   #code.png就是验证码图片
code_result = transform_code_img('./code.png', 1004)
# print(code_result,type(code_result))
ver_code.send_keys(code_result['pic_str'])
bro.find_element_by_name('submit').click()

time.sleep(5)
windows = bro.window_handles   #把新的页面赋值给windows
bro.switch_to.window(windows[-1])   #把窗口windwos中的最后一个窗口为当前窗口
# html = bro.page_source   #提取当前页面网页源码

time.sleep(5)
bro.find_element_by_xpath('//*[@id="sidebar1"]/ul/li[3]/a').click()   #点击到登陆成功之后的页面中的a标签链接
windows = bro.window_handles   #将点击跳转之后的页面赋值给windows
bro.switch_to.window(windows[-1])  #将最后一个窗口当作当前窗口，即跳转之后的页面
page_text = bro.page_source   #提取当前页面网页源码

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
    # run1('10.8.91.153','3306','reptile','3mF5pAXEdoCZJ49c','ads_reptile','Data')
    run1('127.0.0.1','3306','root','qwe123','weifensi','fans')

    # 运行代码时：python 微粉丝数据爬取.py ip port username password database table_name

