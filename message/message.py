import json
import os
import requests
from dotenv import load_dotenv


class Messages(object):
    def __init__(self):
        load_dotenv()

    @classmethod
    def push_plus(cls, **kwargs):
        PUSHPLUS_TOKEN = os.environ["PUSHPLUS_TOKEN"]
        url = 'http://www.pushplus.plus/send'
        data = {
            "token": PUSHPLUS_TOKEN,
            "title": kwargs.get("title"),
            "content": kwargs.get("content"),
            "template": kwargs.get("template"),
            "channel": kwargs.get("channel")
        }
        body = json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type': 'application/json'}
        requests.post(url, data=body, headers=headers)
        print("send push plus success")
