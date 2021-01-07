# coding=utf-8
import json
import requests

# 将此处的机器人hook地址替换为你创建的机器人地址即可
webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=61b95963-c5ce-4777-9f82-75823d29b301"

# 普通 text 文本类型消息
# msgtype: 消息类型，此处为 text
# content: 消息内容，长度 < 2048字节，UTF-8 编码
# mentioned_list: @某个成员，或者@all
# mentioned_mobile_list: @手机号码

text_push_content = """招商银行信用卡的url链接发生了变化"""

text_data = {
    "msgtype": "text",
    "text": {
        "content": text_push_content,
        "mentioned_list": ["@all"]
        # "mentioned_mobile_list": ["@all"]
    }
}


def post_data(url, data):
    # 注意：data发送时，一定要是json格式，另外，字符编码需要是utf-8
    postdata = str(json.dumps(data)).encode('utf-8')
    r = requests.post(url, data=postdata)
    print(r.text)


post_data(webhook_url, text_data)