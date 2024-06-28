import re
import time

import feedparser
import requests
import os
import json
from html import unescape
from bs4 import BeautifulSoup


def fetch_rss(rss, last):
    rss_url = f"https://rss.xbxin.com/rss/telegram/channel/{rss}"
    feed = feedparser.parse(rss_url)
    if not feed.entries:
        print("未找到任何条目。")
        return

    latest_entry = feed.entries[0]
    latest_entry_id = latest_entry.link

    if last != latest_entry_id:
        for entry in feed.entries:
            if entry.link == last:
                break
            if rss == "linux_do_channel":
                send_linux_do(entry)
            else:
                send_push(entry)

        return latest_entry_id

    return last


def send_push(entry):
    msg = f"{entry.title}\n\n{entry.link}\n\n{entry.description}"
    send_msg(msg)


def send_linux_do(entry):
    # 处理标题
    title = entry.title
    match = re.match(r"^(.*?发帖)", title)
    if match:
        title = match.group(1)

    # 处理内容
    description = entry.description
    soup = BeautifulSoup(description, 'html.parser')
    for br in soup.find_all("br"):
        br.replace_with("\n")

    clean_text = soup.get_text()
    clean_text = unescape(clean_text)
    # print(clean_text)
    content_match = re.search(r"发帖\s*(.*)", clean_text, re.DOTALL)

    if content_match:
        clean_text = content_match.group(1).strip()
    # print(clean_text)
    msg = f"{title}\n\n{entry.link}\n\n{str(clean_text)}"
    send_msg(msg)


def read_last_post(post_file):
    try:
        if os.path.exists(post_file):
            with open(post_file, "r") as file:
                data = json.load(file)
                return data
    except:
        # GitHub action
        if os.path.exists(f"mag_push/{post_file}"):
            with open(f"mag_push/{post_file}", "r") as file:
                data = json.load(file)
                return data
    return {}


def write_last_post(post_file, last_post):
    try:
        with open(post_file, "w") as file:
            json.dump(last_post, file)
    except:
        # GitHub action
        with open(f"msg_push/{post_file}", "w") as file:
            json.dump(last_post, file)


def send_msg(message, action="qywx", webhook="H", msg_type="text", url="https://api.xbxin.com/msg"):
    data = {
        "message": message,
        "action": action,
        "webhook": webhook,
        "msg_type": msg_type,
    }

    requests.post(url, json=data)


def main():
    rss_list = ["linux_do_channel"]
    post_file = "last_post.json"
    last_post = read_last_post(post_file)

    for rss in rss_list:
        time.sleep(2)
        last = last_post.get(rss)

        last = fetch_rss(rss, last)
        last_post[rss] = last

    write_last_post(post_file, last_post)


if __name__ == "__main__":
    main()
