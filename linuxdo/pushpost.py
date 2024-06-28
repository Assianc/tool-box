import requests
import feedparser
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def fetch_rss_feed(url, retries=2, timeout=10):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36'
    }
    attempt = 0

    while attempt <= retries:
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                return response.content
            else:
                raise Exception(f"获取RSS源失败: {response.status_code}")
        except requests.exceptions.Timeout:
            print(f"请求超时，正在重试... ({attempt + 1}/{retries + 1})")
            attempt += 1
            if attempt > retries:
                raise Exception("达到最大重试次数，获取RSS源失败。")
            time.sleep(2)


def send_msg(message, action="qywx", webhook="H", msg_type="text", url="https://api.xbxin.com/msg"):
    data = {
        "message": message,
        "action": action,
        "webhook": webhook,
        "msg_type": msg_type,
    }

    requests.post(url, json=data)


def main():
    try:
        with open("latest.txt", "r") as file:
            latest = file.readline().strip()
    except:
        with open("linuxdo/latest.txt", "r") as file:
            latest = file.readline().strip()

    if latest:
        latest = int(latest)
    else:
        latest = 0

    new_latest = latest

    url = 'https://linux.do/latest.rss'
    try:
        rss_content = fetch_rss_feed(url)
        feed = feedparser.parse(rss_content)
        if feed.bozo:
            print("解析Feed出错")
        else:
            for entry in feed.entries:
                soup = BeautifulSoup(entry.summary, "html.parser")
                for tag in soup.find_all(["small", "a"]):
                    tag.decompose()
                text = soup.get_text()
                text = "\n".join(text.splitlines()[:6])
                time_utc8 = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z") + timedelta(hours=8)
                time_str = time_utc8.strftime("%Y-%m-%d %H:%M:%S")
                post_data = f"{entry.title}\n\n{entry.get('author', 'N/A')}  {entry.get('category', 'N/A')}\n\n{text.strip()}\n\n{time_str}\n\n{entry.link}"

                url = "https://linux.do/t/topic/108095"
                # 使用split('/')将字符串分割成列表
                parts = url.split('/')
                # 获取列表中最后一个元素
                post_id = int(parts[-1])

                if post_id > latest:
                    send_msg(post_data)
                    print(post_data)
                else:
                    break

                if post_id > new_latest:
                    new_latest = post_id
            else:
                print("该RSS帖子已发送过，跳过。")
    except Exception as e:
        print(e)

    # 保存最新的文章ID
    try:
        with open('latest.txt', 'w') as file:
            file.write(str(new_latest))
    except:
        with open("linuxdo/latest.txt", "w") as file:
            file.write(str(new_latest))


if __name__ == "__main__":
    main()
