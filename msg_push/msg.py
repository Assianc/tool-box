import base64
import hashlib

import requests


def send_msg(message, action="qywx", webhook="H", msg_type="text", url="https://api.xbxin.com/msg"):
    data = {
        "message": message,
        "action": action,
        "webhook": webhook,
        "msg_type": msg_type,
    }

    requests.post(url, json=data)


# 文本类型
msg = "hello world"
send_msg(msg, url="http://127.0.0.1:8787/msg")
# cf_msg(msg)

# Markdown
# msg = """实时新增用户反馈<font color=\"warning\">132例</font>，请相关同事注意。\n
#          >类型:<font color=\"comment\">用户反馈</font>
#          >普通用户反馈:<font color=\"comment\">117例</font>
#          >VIP用户反馈:<font color=\"comment\">15例</font>"""
# cf_msg(msg, type="markdown", worker_url="http://127.0.0.1:8787/msg")

# 图片类型
# base64
# with open("ikun.png", "rb") as image_file:
#     binary_image = image_file.read()
#     img_base64 = base64.b64encode(binary_image).decode("utf-8")
#
#     hasher = hashlib.md5()
#     hasher.update(binary_image)
#     # 获取MD5
#     img_md5 = hasher.hexdigest()
#
# message = {
#     "base64": img_base64,
#     "md5": img_md5,
# }
# cf_msg(message, type="image", worker_url="http://127.0.0.1:8787/msg")

# 邮件
# message = {
#     "title": "测试邮件",
#     "content": "这是一封测试邮件"
# }
#
# cf_msg(message, method="email", webhook=None, worker_url="http://127.0.0.1:8787/msg")
