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
    github_file = f"/github/{data_file}"
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
    github_file = f"/github/{data_file}"
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

        if events:
            new_event_id = events[0]['id']
            if user not in latest_ids:
                print(f"初始获取{user}的用户活动，不输出任何更新。")
            elif new_event_id != latest_ids[user]:
                for event in events:
                    print(event)
                    if event['id'] == latest_ids[user]:
                        break

                    repo = event['repo']['name']
                    try:
                        commit = event['payload']['commits'][0]['message']
                        message = f"用户: {user} 在仓库: {repo} 提交了更新: {commit}"
                    except:
                        message = f"用户: {user} 在仓库有新的操作"

                    cf_msg(message)

            new_event_ids[user] = new_event_id
    return new_event_ids


def cf_msg(message, method="qywx", webhook="H", type="text", worker_url="https://api.xbxin.com/msg", ):
    data = {
        "method": method,
        "content": {
            "webhook": webhook,
            "type": type,
            "message": message,
        },
    }

    requests.post(worker_url, json=data)


def main():
    users = ['ZhouBinxin']  # GitHub 用户名列表
    data_file = 'data.json'
    latest_ids = read_latest_ids(data_file)
    new_latest_ids = monitor_user_updates(users, latest_ids)
    save_latest_ids(data_file, new_latest_ids)


if __name__ == '__main__':
    main()
