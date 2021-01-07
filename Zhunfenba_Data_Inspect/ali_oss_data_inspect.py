import oss2
import hashlib
import os
import qrcode
from PIL import Image
from Zhunfenba_Data_Inspect import settings

# aa = 'gh_f616cfa0fe7c' #需要加密的字符串
class Upload_Data():
    def __init__(self,ghid_list, i, qrcode_imgurl_list):
        self.ghid_list = ghid_list
        self.i = i
        self.authorizer_qrcode_img_url_list = qrcode_imgurl_list

    #生成md5密文
    def md5Encode(self,str):
        # 创建md5对象
        m = hashlib.md5()
        m.update(str)  # 传入需要加密的字符串进行MD5加密
        return m.hexdigest()  # 获取到经过MD5加密的字符串并返回
    def get_mad(self):
        bb = self.md5Encode(self.ghid_list[self.i].encode('utf-8')) # 必须先进行转码，否则会报错
        return bb

    #生成二维码图片
    def make_img(self):
        qr = qrcode.QRCode(
            version=6,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3,
            border=4.5,
        )  # 设置二维码的大小
        qr.add_data(self.authorizer_qrcode_img_url_list[self.i])
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

                return True
            except:
                return False
        else:
            return False

    def upload_img(self):
        bucket = settings.aliyun_oss()
        try:
            bb = self.get_mad()
            exist = bucket.object_exists(bb +'.png')
            if exist:
                bucket.delete_object(bb +'.png')
                print('原二维码删除成功')
                bucket.put_object_from_file(bb +'.png', bb +'.png')
                print('新二维码上传成功\n')
                os.remove(bb +'.png')
            else:
                bucket.put_object_from_file(bb + '.png', bb + '.png')
                print('二维码上传成功\n')
                os.remove(bb + '.png')

        except:
            print('二维码上传失败\n')


def run(ghid_list,i,qrcode_imgurl_list):
    a = Upload_Data(ghid_list,i,qrcode_imgurl_list)
    a.get_mad()
    img_path = a.make_img()
    a.IsValidImage(img_path)
    a.transimg(img_path)
    a.upload_img()


#判断文件是否存在
# exist = bucket.object_exists(bb)
# # 返回值为true表示文件存在，false表示文件不存在。
# if exist:
#     print('object exist')
# else:
#     print('object not exist')