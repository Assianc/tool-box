import requests


def cf_msg(message, method="qywx", webhook="H", type="text", worker_url="https://api.xbxin.com/msg", ):
    # 构建POST请求的数据
    data = {
        "method": method,
        "content": {
            "webhook": webhook,
            "type": type,
            "message": message,
        },
    }

    # 发送POST请求到Cloudflare Worker
    response = requests.post(worker_url, json=data)

    print(response.text)


# cf_msg("Hello, World!", worker_url="http://127.0.0.1:8787/msg")
cf_msg("Hello, World!")
