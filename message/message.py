import json
import os
import requests
from dotenv import load_dotenv


class Messages(object):
    def __init__(self):
        load_dotenv()

    @classmethod
    def push_plus(cls, **kwargs):
        # message = {
        #     "title": f"天翼云签到推送",
        #     "content": content,
        #     "template": "markdown",
        #     "channel": "wechat"
        # }
        pushplush = os.environ["PUSHPLUS_TOKEN"]
        url = 'http://www.pushplus.plus/send'
        data = {
            "token": pushplush,
            "title": kwargs.get("title"),
            "content": kwargs.get("content"),
            "template": kwargs.get("template"),
            "channel": kwargs.get("channel")
        }
        body = json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json'}
        requests.post(url, data=body, headers=headers)
        print("send push plus success")

    @classmethod
    def wechat(cls, **kwargs):
        # message={
        #     "msgtype": "markdown",
        #     "content": content
        # }
        load_dotenv()
        webhook_url = os.environ["QYAPI"]
        headers = {'Content-Type': 'application/json'}
        payload = {
            "msgtype": kwargs.get("msgtype"),
            kwargs.get("msgtype"): {
                "content": kwargs.get("content")
            }
        }

        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
        print(response.text)

    @classmethod
    def cf_worker(cls, message, api_type='default', worker_url='https://qyapi.bxin.top/'):
        """
        通过Cloudflare Worker发送消息，基于企业微信机器人

        :param api_type: 发送消息使用的webhook，默认为 default，发送课表使用course
        :param message:
        :param worker_url: worker地址
        :return:
        """
        # 构建POST请求的数据
        data = {
            'type': api_type,
            'message': message,
        }

        # 发送POST请求到Cloudflare Worker
        response = requests.post(worker_url, json=data)

        # 检查响应状态码
        if response.ok:
            print('Message sent successfully')
        else:
            print('Failed to send message')
