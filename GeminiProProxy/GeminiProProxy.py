import requests


def gemini(content):
    # 定义请求的 URL
    url = "https://gemini.bxin.top/v1beta/models/gemini-pro:generateContent?key=AIzaSyAk3B8oqFNlkMtVkxwbYfPD_XOH3GGiNl4"

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
