import sys
import time
# print('[%-15s]' %'#')
# print('[%-15s]' %'##')
# print('[%-15s]' %'###')
# print('[%-15s]' %'####')
# print('%s%%' %(100))
#
# def progress(percent):
#     if percent > 1:
#         percent=1
#     res = int(50 * percent) * '#'
#     print('\r[%-50s]%d%%' % (res, int(percent * 100)), end='')
#
# recv_size = 0
# total_size = 333200
# while recv_size < total_size:
#     time.sleep(0.05)
#     recv_size+=1024
#     percent=recv_size/total_size
#     progress(percent)

# print(time.time())
# import random
# code_source = '0123456789'
# ran_num = ''
# for i in range(16):
#     # 随机选择一个字符
#     s = code_source[random.randrange(0, len(code_source) - 1)]
#     ran_num += s
# timestamp = str(int(time.time() * 1000))
# print(type(ran_num))


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
login_url = 'https://buss.weifenshi.cn/index.php/buss/index'
page_text = requests.get(url=login_url,headers=headers).text
tree = etree.HTML(page_text)
img_path = 'https://buss.weifenshi.cn' + tree.xpath('//*[@id="captchaImg"]/@src')[0]
img_data = requests.get(url=img_path, headers=headers).content  # 请求到了图片数据
with open('./code.jpg', 'wb') as fp:
    fp.write(img_data)
code_result = verification_code_rec('./code.jpg', 1004)

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
url = 'https://buss.weifenshi.cn/index.php/buss/index'
response = weifensiSession.get(url=url,headers=headers)
print(response.text)