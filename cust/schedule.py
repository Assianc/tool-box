import json
import os

import requests
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()
pushplush = os.environ["PUSHPLUS_TOKEN"]
key = os.environ['GEMINI_KEY']


def get_data():
    cookies = {
        'JSESSIONID': 'b0896545-ada7-4a4a-8edf-12bed26cec25',
        'wengine_new_ticket': '94ac39b143f32d5f',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Referer': 'https://kbpro.cust.edu.cn/Schedule/index.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320',
    }

    try:
        response = requests.get('https://kbpro.cust.edu.cn/Schedule/getSchedulejson', cookies=cookies, headers=headers)
        with open("data.json", "w") as json_file:
            json.dump(json.loads(response.text), json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(e)
        return False


def read_data():
    with open("cust/data.json", "r") as json_file:
        return json.load(json_file)


def parse(courses):
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    weekday = tomorrow.weekday()
    content = ''

    start_date = datetime(2024, 2, 26)
    days_diff = (tomorrow - start_date).days + 1
    week_number = days_diff // 7
    if days_diff % 7 != 0:
        week_number += 1

    # print(courses)
    for course in courses:
        # print(course)
        if int(course['dayOfWeek']) - 1 == weekday and course['weekDescription'][week_number] == '1':
            content += f"""
            {course['courseName']}
            {course['classroomName']}
            {course['beginSection']}~{course['endSection']}节
            {course['teacherName']}
            """
    return content


def push_plus(**kwargs):
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
    print("send pushplus success")


def gemini(content):
    # 定义请求的 URL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={key}"

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

    try:
        response = response.json()
        return response['candidates'][0]['content']['parts'][0]['text']
    except requests.exceptions.JSONDecodeError as e:
        print("JSON 解码错误:", e)
        print("响应内容:", response.text)
        return "明天没课啦！"


def main():
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    content = None
    if tomorrow.weekday() < 5:
        courses = read_data()
        content = parse(courses)

    if not content:
        content = gemini('使用中文为一名大学生，写一段庆祝一天没有课程的文案！')

    message = {
        "title": "课表推送",
        "content": content,
        "template": "markdown",
        "channel": "wechat"
    }
    push_plus(**message)


if __name__ == '__main__':
    # get_data()
    # print(os.listdir("."))
    main()
