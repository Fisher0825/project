import qrcode
from PIL import Image
import os
def make_img():
    qr = qrcode.QRCode(
        version=6,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=3,
        border=5,
    )#设置二维码的大小
    qr.add_data("http://weixin.qq.com/r/5B1NVQHEQFw-rUU290j2")
    qr.make(fit=True)
    img = qr.make_image()
    img_name = ('%s')%'图片.png'
    img.save(img_name)

    img_path = os.path.abspath(img_name)
    return img_path

def IsValidImage(img_path):
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
def transimg(img_path):
    """
    转换图片格式
    :param img_path:图片路径
    :return: True：成功 False：失败
    """
    if IsValidImage(img_path):
        try:
            str = img_path.rsplit(".", 1)
            output_img_path = str[0] + ".jpg"
            print(output_img_path)
            im = Image.open(img_path).resize((150, 150), Image.BILINEAR)
            im.save(output_img_path)
            #对旧的.png文件删除
            os.remove(img_path)
            #再对新的文件名进行替换
            os.rename(str[0] + ".jpg", '图片'+'.'+'png')  # 重命名,覆盖原先的名字
            return True
        except:
            return False
    else:
        return False
if __name__ == '__main__':
    img_path = make_img()
    print(transimg(img_path))

