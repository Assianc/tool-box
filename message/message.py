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
        #}
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
