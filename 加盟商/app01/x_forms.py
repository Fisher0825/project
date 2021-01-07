# --*-- coding: utf-8 --*--
# @Author: Fangyu
# @Email:fangyu@tiancan.tech
# @Time: 2021/1/6 15:39
# @File: x_forms.py
from django.core.exceptions import ValidationError
from django.forms import widgets
from django import forms
from app01 import models


class FormRegister(forms.Form):
    username = forms.CharField(
        required=True,
        max_length=45,
        min_length=3,
        label='<i class="layadmin-user-login-icon layui-icon layui-icon-username" for="LAY-user-login-nickname"></i>',
        error_messages={
            'required': '用户名不能为空',
            'min_length': "用户名最少3位",
            'max_length': "用户名最大45位"
        },
        widget=widgets.TextInput(attrs={'placeholder':'用户名','class':'layui-input',}),
    )
    mobile = forms.CharField(
        required=True,
        max_length=13,
        min_length=13,
        label='<i class="layadmin-user-login-icon layui-icon layui-icon-cellphone" for="LAY-user-login-cellphone"></i>',
        error_messages={
            'required': '手机号码不能为空'
        },
        widget=widgets.TextInput(attrs={'placeholder':'手机' ,'class':'layui-input','name':'mobile' ,'id':'LAY-user-login-cellphone'}),

    )
    password = forms.CharField(
        required=True,
        max_length=32,
        min_length=3,
        label='<i class="layadmin-user-login-icon layui-icon layui-icon-password" for="LAY-user-login-password"></i>',
        error_messages={
            'required': '密码不能为空',
            'min_length': "密码最少3位",
            'max_length': "密码最大32位"
        },
        widget=widgets.PasswordInput(attrs={'placeholder':'密码', 'class':'layui-input','name':'password'}),
    )
    re_password = forms.CharField(
        required=True,
        max_length=32,
        min_length=3,
        label='<i class="layadmin-user-login-icon layui-icon layui-icon-password" for="LAY-user-login-repass"></i>',
        error_messages={
            'required': '确认密码不能为空',
            'min_length': "密码最少3位",
            'max_length': "密码最大32位"
        },
        widget=widgets.PasswordInput(attrs={'placeholder':'确认密码', 'class':'layui-input', 'name':'repass'}),
    )


    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = models.Dim_franchisee_account_employee.objects.filter(username=username).exists()
        if user:
            raise ValidationError('该用户名已存在')
        else:
            return username

    def clean(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password == re_password:
            return self.cleaned_data
        else:
            raise ValidationError('两次密码不一致')