import os
import requests
from dotenv import load_dotenv


class Gemini(object):
    @classmethod
    def chat(cls, prompt):
        load_dotenv()
        keys = os.environ['GEMINI_KEY'].split(',')

        # 定义要发送的 JSON 数据
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        # 定义请求头
        headers = {
            "Content-Type": "application/json"
        }

        response = None

        for i in range(len(keys)):
            key = keys[i]
            # 定义请求的 URL
            url = f"https://gemini.bxin.top/v1beta/models/gemini-pro:generateContent?key={key}"

            # 发送 POST 请求
            response = requests.post(url, json=data, headers=headers)
            response = response.json()
            try:
                response = response['candidates'][0]['content']['parts'][0]['text']
                break
            except Exception as e:
                print(f"Error: {e}")
                response = 'error'

        return response


if __name__ == '__main__':
    content = "hello"
    result = Gemini.chat(content)
    print(result)
