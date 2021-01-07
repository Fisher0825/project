#!/usr/bin/python3
# --*-- coding: utf-8 --*--
# @Author: Fangyu
# @Email: 327520514@qq.com
# @Time: 2020/11/18 14:08
# @File: send_msg.py
# @Software: PyCharm
import json
import requests
class Send_msg():
    def __init__(self,authorizer_nickname):
        self.authorizer_nickname = authorizer_nickname
        self.webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=f2374acd-156b-4b90-ab11-67b2781b3bb5"
        self.text_push_content1 = """%s号源信息已经下线""" % self.authorizer_nickname['authorizer_nickname']
        self.text_push_content2 = """%s号源信息已经上线""" % self.authorizer_nickname['authorizer_nickname']

        self.text_data1 = {
            "msgtype": "text",
            "text": {
                "content": self.text_push_content1,
                #需要@谁就将谁的名字小写放在这里，如果是所有人需要加上@ eg:"@all",@个人不需要加
                "mentioned_list": ["fangyu"]
            }
        }
        self.text_data2 = {
            "msgtype": "text",
            "text": {
                "content": self.text_push_content2,
                # 需要@谁就将谁的名字小写放在这里，如果是所有人需要加上@ eg:"@all",@个人不需要加
                "mentioned_list": ["xuejian"]
            }
        }
    def post_data1(self):
        # 注意：data发送时，一定要是json格式，另外，字符编码需要是utf-8
        postdata = str(json.dumps(self.text_data1)).encode('utf-8')
        r = requests.post(self.webhook_url, data=postdata)
        # print(r.text)
        print('%s下线消息已通知'%self.authorizer_nickname['authorizer_nickname'])
        print(' ')
    def post_data2(self):
        # 注意：data发送时，一定要是json格式，另外，字符编码需要是utf-8
        postdata = str(json.dumps(self.text_data2)).encode('utf-8')
        r = requests.post(self.webhook_url, data=postdata)
        print('\n%s上线消息已通知\n'%self.authorizer_nickname['authorizer_nickname'])
def run1(authorizer_nickname):
    a = Send_msg(authorizer_nickname)
    a.post_data1()
def run2(authorizer_nickname):
    a = Send_msg(authorizer_nickname)
    a.post_data2()