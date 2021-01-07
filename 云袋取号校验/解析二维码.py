import os
import requests
from io import BytesIO
from pyzbar import pyzbar
from PIL import Image, ImageEnhance
def get_ewm(img_adds):

    rq_img = requests.get(img_adds).content
    img = Image.open(BytesIO(rq_img))

    # img.show()  # 显示图片，测试用

    txt_list = pyzbar.decode(img)

    for txt in txt_list:
        barcodeData = txt.data.decode("utf-8")
        print(barcodeData)


if __name__ == '__main__':
    get_ewm('https://client.yunfenba.com/public/upload/2020-10-31/1604129862.png')