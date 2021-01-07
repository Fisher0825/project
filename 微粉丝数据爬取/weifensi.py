import requests
import time
import re
import random
import threading
import pymysql
from lxml import etree
from 微粉丝数据爬取 import chaojiying
# 禁用安全请求警告。
requests.packages.urllib3.disable_warnings()


class WeiFenShi(object):
    def __init__(self, username, password):
        self.session = requests.Session()
        self.username = username
        self.password = password

    def get_image(self):
        '''获取验证码'''
        url = 'https://buss.weifenshi.cn/index.php/index/verify'
        response = self.session.get(url, verify=False)
        with open('code.png', 'wb') as f:
            f.write(response.content)
        # print('图片验证码已识别')
    def check_image(self):
        '''识别验证码, 调用打码平台【超级鹰】'''
        code = chaojiying.transform_code_img('code.png', 1004)
        code = code['pic_str']
        # print(code)
        return code

    def login(self, code):
        '''登录'''
        code_source = '0123456789'
        ran_num = ''
        for i in range(16):
            # 随机选择一个字符
            s = code_source[random.randrange(0, len(code_source) - 1)]
            ran_num += s
        timestamp = str(int(time.time() * 1000))
        url = 'https://buss.weifenshi.cn/index.php/index/check_login?callback=jQuery1910{}_{}&username={}&password={}&verify_code={}&_={}'.format(ran_num, timestamp, self.username, self.password, code, timestamp)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
            'Referer': 'https://buss.weifenshi.cn/',
            'Host': 'buss.weifenshi.cn'
        }
        print('正在登录')
        response = self.session.get(url, headers=headers, verify=False)
        return response

    def check_login(self, response):
        '''判断是否登录成功'''
        status = re.findall(r'"status":(\d+),', response.text, re.S)
        try:
            if status[0] == '1':
                print('登录成功！')
            else:
                print('登录失败！')
        except Exception as e:
            print(e)

    def get_index(self):
        '''请求首页'''
        url = 'https://buss.weifenshi.cn/index.php/buss/summary'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
            'Referer': 'https://buss.weifenshi.cn/',
            'Host': 'buss.weifenshi.cn'
        }
        response = self.session.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            html = response.text
            return html
        return None

    def parse_index(self, html):
        '''解析网页'''
        selector = etree.HTML(html)
        today_earnings = selector.xpath('//*[@id="main_1"]/div[1]/div/dl[1]/dd/text()')[0]
        today_fans = selector.xpath('//*[@id="main_1"]/div[1]/div/dl[2]/dd/text()')[0]
        month_fans = selector.xpath('//*[@id="main_1"]/div[1]/div/dl[3]/dd/text()')[0]
        total_fans = selector.xpath('//*[@id="main_1"]/div[1]/div/dl[4]/dd/text()')[0]
        print(' 今日收益:', today_earnings,'\n','今日带粉:',today_fans,'\n','本月带粉:',month_fans,'\n','总带粉数:',total_fans)
        # time_stamp = str(int(time.time() * 1000))
        time_stamp = time.strftime("%Y-%m-%d %X")
        print('时间:', time_stamp)
        return today_earnings, today_fans, month_fans, total_fans, time_stamp

    def save_data(self, today_earnings, today_fans, month_fans, total_fans, time_stamp):
        '''保存到mysql数据库'''
        # 创建connection连接
        conn = pymysql.connect(host='127.0.0.1', port=3306, database='weifensi', user='root', password='qwe123',charset='utf8')
        # 获取cursor对象
        cs1 = conn.cursor()
        # 执行sql语句
        query = 'insert into `fans`(today_earnings, today_fans, month_fans, total_fans,time_stamp) values(%s, %s, %s, %s, %s)'
        values = (today_earnings, today_fans, month_fans, total_fans, time_stamp)
        cs1.execute(query, values)
        # 提交之前的操作，如果之前已经执行多次的execute，那么就都进行提交
        conn.commit()
        # 关闭cursor对象
        cs1.close()
        # 关闭connection对象
        conn.close()

    def run(self):
        # 获取图片验证码
        self.get_image()
        # 识别图片验证码
        code = self.check_image()
        # 登录
        response = self.login(code)
        # 判断是否登录成功
        self.check_login(response)

    def fun_timer(self):
        '''每隔5分钟执行一次'''
        print('==========每隔5分钟执行一次===========')
        # 请求首页
        html = self.get_index()
        today_earnings, today_fans, month_fans, total_fans, time_stamp = self.parse_index(html)
        # 入库
        self.save_data(today_earnings, today_fans, month_fans, total_fans, time_stamp)
        global timer
        timer = threading.Timer(300, self.fun_timer)  # 300秒
        timer.start()


if __name__ == '__main__':
    # 账号和密码
    a = WeiFenShi('tckj', 'tckj008008')
    a.run()
    timer = threading.Timer(1, a.fun_timer)
    timer.start()

