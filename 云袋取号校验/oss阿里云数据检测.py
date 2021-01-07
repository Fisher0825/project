import oss2
import hashlib
import os
import qrcode
from PIL import Image

class Upload_Data():
    def __init__(self,gh_id_list,i,authorizer_qrcode_link_list):
        self.gh_id_list = gh_id_list
        self.i = i
        self.authorizer_qrcode_link_list = authorizer_qrcode_link_list
    #生成md5密文
    def md5Encode(self,str):
        # 创建md5对象
        m = hashlib.md5()
        m.update(str)  # 传入需要加密的字符串进行MD5加密
        return m.hexdigest()  # 获取到经过MD5加密的字符串并返回
    def get_mad(self):
        bb = self.md5Encode(self.gh_id_list[self.i].encode('utf-8')) # 必须先进行转码，否则会报错
        return bb

    #生成二维码图片
    def make_img(self):
        qr = qrcode.QRCode(
            version=6,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3,
            border=4.5,
        )  # 设置二维码的大小
        qr.add_data(self.authorizer_qrcode_link_list[self.i])
        qr.make(fit=True)
        img = qr.make_image()
        img_name = ('%s') % (self.get_mad() +'.png')
        img.save(img_name)
        img_path = os.path.abspath(img_name)
        return img_path
    def IsValidImage(self,img_path):
        """
        判断文件是否为有效（完整）的图片
        :param img_path:图片路径
        :return:True：有效 False：无效
        """
        bValid = True
        try:
            Image.open(img_path).verify()
        except:
            bValid = False
        return bValid
    def transimg(self,img_path):
        """
        转换图片格式
        :param img_path:图片路径
        :return: True：成功 False：失败
        """
        if self.IsValidImage(img_path):
            try:
                str = img_path.rsplit(".", 1)
                output_img_path = str[0] + ".jpg"
                im = Image.open(img_path).resize((150, 150), Image.BILINEAR)
                im.save(output_img_path)
                # 对旧的.png文件删除
                os.remove(img_path)
                # 再对新的文件名进行替换
                os.rename(str[0] + ".jpg", self.get_mad() + '.' + 'png')  # 重命名,覆盖原先的名字
                os.remove(self.get_mad() + '.' + 'png')
                return True
            except:
                return False
        else:
            return False

    def upload_img(self):

        # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
        auth = oss2.Auth('LTAI4G5VUWNavHFqPJucReLo', '3BRXG5pK806NTlrBL0UHGcuC8SIZEJ')
        bucket = oss2.Bucket(auth, 'http://oss-cn-hongkong.aliyuncs.com', 'resjinguidnacom')
        try:
            bb = self.get_mad()
            exist = bucket.object_exists(bb)
            if exist:
                bucket.delete_object(bb)
                print('原二维码删除成功')
                bucket.put_object_from_file(bb + '.png', bb + '.png')
                print('新二维码上传成功')
                print(' ')
            else:
                bucket.put_object_from_file(bb + '.png', bb + '.png')
                print('二维码上传成功')
                print(' ')

        except:
            print('文件上传失败')
            print(' ')
            # print('文件删除失败')

def run(gh_id_list,i,authorizer_qrcode_link_list):
    a = Upload_Data(gh_id_list,i,authorizer_qrcode_link_list)
    a.get_mad()
    img_path = a.make_img()
    a.IsValidImage(img_path)
    a.transimg(img_path)
    a.upload_img()