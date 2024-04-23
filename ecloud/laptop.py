# -*- coding: utf-8 -*-
import requests
import time
from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()
path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'  # 请改为你电脑内Chrome可执行文件路径
co.set_browser_path(path)
co.headless(True)
page = ChromiumPage(co)


def login():
    page.get('https://pc.ctyun.cn/#/login')

    try:
        # 定位到账号文本框并输入账号
        page.ele('@class=account').input('xxx')
        # 定位到密码文本框并输入密码
        page.ele('@class=password').input('xxx')

        # 尝试定位验证码
        captcha = page.ele('#el-id-6762-4')

        if captcha:
            img = page.ele('@class=box-form-item-code')
            img.get_screenshot()
            bytes_str = img.get_screenshot(as_bytes='png')

            cf_worker(bytes_str)

            # 等待用户输入验证码
            captcha_code = input("请输入验证码：")

        # 点击登录按钮
        page.ele('@class=form-item right-body__submit').click()
    except:
        pass


def keep_alive():
    page.ele('@class=desktop-main-entry').click()

    # 等待页面加载完成
    page.wait(10)

    page.close()


def cf_worker(message, method="qywx", api_type="default", msgtype="text", worker_url="https://qyapi.bxin.top/msg",
              webhook=None):
    # 构建POST请求的数据
    data = {
        "method": method,
        "content": {
            "type": api_type,
            "msgtype": msgtype,
            "message": message,
            "webhook": webhook,
        },
    }

    # 发送POST请求到Cloudflare Worker
    try:
        requests.post(worker_url, json=data)
    except:
        pass


def main():
    while True:
        try:
            login()
            keep_alive()
            cf_worker("keep alive success")
            # 等待40分钟
            time.sleep(40 * 60)
        except Exception as e:
            cf_worker("keep alive error")
            cf_worker(str(e))
            time.sleep(5 * 60)


if __name__ == '__main__':
    main()
