import os

import requests
from dotenv import load_dotenv


def gemini(content):
    load_dotenv()
    key = os.environ['GEMINI_KEY']
    # 定义请求的 URL
    url = f"https://gemini.bxin.top/v1beta/models/gemini-pro:generateContent?key={key}"

    # 定义要发送的 JSON 数据
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": content
                    }
                ]
            }
        ]
    }

    # 定义请求头
    headers = {
        "Content-Type": "application/json"
    }

    # 发送 POST 请求
    response = requests.post(url, json=data, headers=headers)

    # 输出响应结果
    return response.json()


if __name__ == '__main__':
    content = "明天是周末，没有课，使用作为写一段庆祝的话"
    result = gemini(content)
    print(result)
