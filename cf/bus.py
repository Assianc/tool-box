import requests


def bus(content, worker_url="https://api.bxin.top/bus", ):
    # 构建POST请求的数据
    data = {"content": content, "id": "101"}

    # 发送POST请求到Cloudflare Worker
    response = requests.post(worker_url, json=data)

    print(response.text)


def main():
    # bus("lines", worker_url="http://127.0.0.1:8787/bus")
    bus("lines")
    # cf_worker('test')


if __name__ == "__main__":
    main()
