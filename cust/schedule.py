import json

import requests
from datetime import datetime, timedelta


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
    try:
        with open("./data.json", "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except:
        # GitHub action
        with open("cust/data.json", "r", encoding="utf-8") as json_file:
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
            content += f"{course['courseName']}\n{course['classroomName']}\n{course['beginSection']}~{course['endSection']}节\n{course['teacherName']}\n"
    return content


def send_msg(message, action="qywx", webhook="H", msg_type="text", url="https://api.xbxin.com/msg"):
    data = {
        "message": message,
        "action": action,
        "webhook": webhook,
        "msg_type": msg_type,
    }

    requests.post(url, json=data)


def main():
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    content = None
    if tomorrow.weekday() < 5:
        courses = read_data()
        content = parse(courses)

    if content is None:
        content = '明天没课啦'

    send_msg(content, webhook='M')


if __name__ == '__main__':
    # get_data()
    # print(os.listdir("."))
    main()
