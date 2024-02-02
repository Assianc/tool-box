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
                        "text": "尽可能使用中文回复 " + content
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

    data = response.json()

    try:
        data = data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        data = "抱歉，我无法理解你的问题，请换一种方式问我。"
    # 输出响应结果
    return data


if __name__ == '__main__':
    print(gemini("什么时候去ktv看我表演"))
