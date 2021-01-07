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
    def __init__(self,nickname_list,i):
        self.nickname_list = nickname_list
        self.i = i
        self.webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=f2374acd-156b-4b90-ab11-67b2781b3bb5"
        self.text_push_content = """%s号源信息已经更新""" % self.nickname_list[i]
        self.text_data = {
            "msgtype": "text",
            "text": {
                "content": self.text_push_content,
                #需要@谁就将谁的名字小写放在这里，如果是所有人需要加上@ eg:"@all",@个人不需要加
                "mentioned_list": ["fangyu"]
            }
        }
    def post_data(self):
        # 注意：data发送时，一定要是json格式，另外，字符编码需要是utf-8
        postdata = str(json.dumps(self.text_data)).encode('utf-8')
        r = requests.post(self.webhook_url, data=postdata)
        # print(r.text)
        print('%s数据更新消息已通知\n'%self.nickname_list[self.i])
def run(nickname_list,i):
    a = Send_msg(nickname_list,i)
    a.post_data()