import requests
from hashlib import md5
from lxml import etree
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        }
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
    im = open(imgpath, 'rb').read()#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    return chaojiying.PostPic(im, imgtype)#1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()

sess = requests.Session() #创建好session对象
login_url = 'https://buss.weifenshi.cn/'
page_text = sess.get(url=login_url,headers=headers).text
tree = etree.HTML(page_text)
#解析出验证码图片的地址
img_path = 'https://buss.weifenshi.cn'+tree.xpath('//*[@id="captchaImg"]/@src')[0]
img_data = sess.get(url=img_path,headers=headers).content #请求到了图片数据

#将图片保存到本地存储
with open('./code.jpg','wb') as fp:
    fp.write(img_data)



