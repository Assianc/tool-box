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
    with open("data.json", "r") as json_file:
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

    if content:
        message = {
            "title": "课表推送",
            "content": content,
            "template": "markdown",
            "channel": "wechat"
        }
        push_plus(**message)
        return True
    else:
        return False


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


def main():
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    content = None
    if tomorrow.weekday() < 5:
        courses = read_data()
        if not parse(courses):
            content = gemini("""
            使用中文
            明天是周末，写一段庆祝的话！
            对象是一个大学生
            """)
    else:
        content = gemini('明天没有课，使用中文写一段庆祝的话！')

    if content:
        content = content['candidates'][0]['content']['parts'][0]['text']
        message = {
            "title": "课表推送",
            "content": content,
            "template": "markdown",
            "channel": "wechat"
        }
        push_plus(**message)


if __name__ == '__main__':
    # get_data()
    main()
