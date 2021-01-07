from django.shortcuts import render , HttpResponse ,redirect
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from app01 import x_forms

import random
# Create your views here.
def center(request):
    return render(request,'center.html')

def home(request):
    return render(request,'home.html')

def Franchisee_Orders(request):
    return render(request,'Franchisee_Orders.html')

def register(request):
    if request.method == 'GET':
        form = x_forms.FormRegister()
        return render(request,'register.html',locals())
    return render(request,'register.html')


def login(request):

    return render(request,'login.html')

def index(request):

    return render(request,'index.html')

# 获取随机颜色
def get_rgb():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
# 获取验证码
def get_valid_code(request):
    img = Image.new('RGB', (200, 38), get_rgb())
    img_draw = ImageDraw.Draw(img)
    img_font = ImageFont.truetype('./static/font/FZFenSTXJW.TTF', 25)
    valid_code = ''
    for i in range(5):
        low_char = chr(random.randint(97, 122))
        num_char = random.randint(0, 9)
        upper_char = chr(random.randint(65, 90))
        res = random.choice([low_char, num_char, upper_char])
        valid_code += str(res)
        img_draw.text((i * 40 + 10, 5), str(res), get_rgb(), img_font)
    request.session['valid_code'] = valid_code
    print(valid_code)

    f = BytesIO()
    img.save(f, 'png')
    data = f.getvalue()
    return HttpResponse(data)


