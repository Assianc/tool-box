import requests
import json
import os
from environs import Env


def read_latest_ids(data_file):
    """
    读取最新的事件ID
    :param data_file:
    :return:
    """
    # Github action
    github_file = f"github/{data_file}"
    if os.path.exists(github_file):
        with open(github_file, 'r') as f:
            return json.load(f)
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return json.load(f)
    return {}


def fetch_latest_events(user):
    """
    获取用户最近的活动
    :param user:
    :return:
    """
    env = Env()
    env.read_env()
    token = env.str('PERSONAL_ACCESS_TOKEN')
    url = f'https://api.github.com/users/{user}/events'
    HEADERS = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        cf_msg(f"Error fetching events for {user}: {response.status_code}")
        return []


def save_latest_ids(data_file, latest_ids):
    """
    将最新的事件ID保存到文件中
    :param data_file:
    :param latest_ids:
    :return:
    """
    # Github action
    github_file = f"github/{data_file}"
    try:
        with open(github_file, 'w') as f:
            json.dump(latest_ids, f)
    except:
        with open(data_file, 'w') as f:
            json.dump(latest_ids, f)


def monitor_user_updates(users, latest_ids):
    """
    监控用户活动
    :return:
    """
    new_event_ids = latest_ids.copy()

    for user in users:
        events = fetch_latest_events(user)
        messages = ''
        if events:
            new_event_id = events[0]['id']
            if user not in latest_ids:
                print(f"初始获取{user}的用户活动，不输出任何更新。")
            elif new_event_id != latest_ids[user]:
                for event in events:
                    print(event)
                    if event['id'] == latest_ids[user]:
                        break

                    created_at = event['created_at']
                    event_type = event['type']
                    repo = event['repo']['name']

                    message = f"{created_at}\n仓库：{repo}\n"
                    if event_type == 'PushEvent':
                        # 提交信息
                        message += f"提交信息：{event['payload']['commits'][0]['message']}"
                    elif event_type == 'DeleteEvent':
                        # 删除信息
                        message += f"删除信息：{event['payload']['ref_type']} {event['payload']['ref']} was deleted"
                    elif event_type == 'CreateEvent':
                        # 创建信息
                        message += f"创建信息：{event['payload']['ref_type']} {event['payload']['ref']} was created"
                    else:
                        # 事件类型
                        message += f"事件类型：{event_type}\n"
                        # 未处理
                        message += f"未处理：{event['payload']}"

                    messages += message + "\n——————————"
            new_event_ids[user] = new_event_id
        cf_msg(messages)
    return new_event_ids


def cf_msg(message):
    url = 'https://hono-kit.azure334792.workers.dev/msg/admin/corp'

    data = {
        "title": "Github MSG",
        "desc": "每日信息",
        "content": message,
    }

    requests.post(url, json=data)


def main():
    users = ['ZhouBinxin', 'sakura-ryoko', 'Fallen-Breath']  # GitHub 用户名列表
    data_file = 'data.json'
    latest_ids = read_latest_ids(data_file)
    new_latest_ids = monitor_user_updates(users, latest_ids)
    save_latest_ids(data_file, new_latest_ids)


if __name__ == '__main__':
    main()
