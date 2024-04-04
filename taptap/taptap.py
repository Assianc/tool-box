import datetime
import json
import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from dotenv import load_dotenv

load_dotenv()

# 邮件推送的配置信息
smtp_server = 'smtp.163.com'  # SMTP 服务器地址
smtp_port = 25  # SMTP 服务器端口号
sender_email = os.environ['SENDER_EMAIL']
sender_password = os.environ['SENDER_PASSWORD']
receiver_email = '1277544694@qq.com'  # 收件人邮箱


def getdata():
    headers = {
        'authority': 'www.taptap.cn',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        # 'cookie': 'web_app_uuid=d82a5cb9-eb89-4547-82bb-696b8d5963d9; Hm_lvt_536e39e029b26af67aecbc444cdbd996=1710228372; apk_download_url_postfix=/organic-direct_index; _clck=121pm3g%7C2%7Cfk0%7C0%7C1532; acw_tc=7b39758217104621214596757eca0ef56e7d6c7eb21be5148bd4f060f2276a; XSRF-TOKEN=0zsrzzl8eaynkw7wyuxc; locale=zh_CN; tap_theme=light; ssxmod_itna2=WqjE7KBKiKD5Y5GHD8D2eLE3DIoOagnjmexUxnK3224DseoqDLe9QN=nQB4nbRjPcbBwqU8e3FO9xmPoQq8pK/FQO963oMpOK6EaHz64XzdG9QwXo=xf9Qn2kHnQ=rukIpHMTZqZxczy6mGPg5sg2aiqWhdo3e+u79so3vwbIKaoUWm3f9IzcAiTbIddQ8TKlGdai7=LK7=5BR=Mc7TPS35qj2p394L5U0qoEMDu3emP5nsSbe=ibmUox4vTQ9DoQr7HOI4zO0dZeMjwMy9VCBfZCazATuzagy1iFTqZIvibunQece=Wg3DnPcEsI+OWx8KmKHh3aAhxEHNGsXBKqj5nDNcBQWE557+n7d5BK4Ew5AGpRwB3Y/BkgEQvnN1n3Rj31LhaorEfYy0w7EN7CKLwQb3mPOWBmd=oAq3rHnYjMvC2EKj5Tnvq8or6wipKO6Ab6abbsPhfygfHeYTSti2v1jkmar3+Lb8oexWujIT3fk2an1bn=Nq4Th1jKeWLSrr2H=gxADDw=h=jx5374niKtO58ydwP8lG3ww=Qr6jvoi5FoIrwmZjG=DGcDG7BMzQ3ckGD4D==; tfstk=f9VI16YKUHxCBwkp3zQal6QJ3SlSOk1VAUg8ozdeyXhp23UxbQ7na0l7ycZoUD3EYQM-X4gJ9pHpWF3r9Y2E4DoSNzqf7i5Vgy4nZfIV0sud3gkEiQnJp3l9B4A_XaTVgy4HWAH_wCf2N2BDZLi82vh9Bqn9w4h82fCtucdKyB3JXNgkutjWOIOTPGOetQc4cUu1jWNL12MtQyitGjQr-vZ_JcgiS5O-dmUKfQIf7G_rVcVAbOagPJEESu1fffUYCX3Q2spqXRaTtxlfHpZY7kVj9SsBTVkSARFKCUd8Wfm_m8ZCApmLLlMmWAL5iVrqXyVLCaxTJooI9VHNMZategu9gm1X5LTsnQgs0N_6ELA2Zag-4u7KCv3iSE715KJopV0s0N_6ELDKSVfV5N92E; ssxmod_itna=mui=BKeIxAxmxBPqeqCzID77DkCTIwxDCKjjDBkfD4iNDnD8x7YDvG+OKuGCRC3mOnxWxa722tW5lh+hxWCWmxPaz5xCPGnDBI+YT+DYA8Dt4DTD34DYDirQGIDieDFF5H/8DbxYQDmxiODlKH6xDa0xi3LaKDR25D0Z+FDQKDugFKDGHK1I2eC00Qd3vF=4YpDiv4R=2eLxG1F40HPQkKLxo69Ih1R2fLo+bO43YDvxDkDUKDo2PpDB+kBp7NQG+qQDxNoxrxfA0ep0iK3e8NtGxK30/a5irKqmnYCC4NamhDD=',
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': 'https://www.taptap.cn/user/12391881',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        'x-requested-with': 'XMLHttpRequest',
        'x-xsrf-token': '0zsrzzl8eaynkw7wyuxc',
    }

    params = {
        'id': '12391881',
        'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=102&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=d82a5cb9-eb89-4547-82bb-696b8d5963d9&DT=PC&OS=Windows&OSV=15.0.0',
    }

    response = requests.get('https://www.taptap.cn/webapiv2/user/v1/detail', params=params, headers=headers)
    return response.json()


def cf_worker(message, method='qywx', api_type='default', worker_url='https://qyapi.bxin.top/'):
    # 构建POST请求的数据
    data = {
        'method': method,
        'content': {
            'type': api_type,
            'message': message,
        }
    }

    # 发送POST请求到Cloudflare Worker
    requests.post(worker_url, json=data)


def create_message(data):
    title = 'TapTap推送'
    name = data.get('data').get('name')
    time = data.get('data').get('stat').get('spent_tips')

    now = datetime.datetime.now()
    content = f"""
    游戏时间：{time}
    昵称：{name}
    查询时间：{now.strftime('%Y-%m-%d %H:%M:%S')}
    """
    cf_worker(content)


def send_email(subject, content):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = Header(subject, 'utf-8')

    text_part = MIMEText(content, 'plain', 'utf-8')
    msg.attach(text_part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 开启安全连接
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("邮件发送成功")
    except Exception as e:
        print("邮件发送失败:", str(e))
    finally:
        if 'server' in locals():
            server.quit()


def main():
    data = getdata()
    create_message(data)


if __name__ == '__main__':
    main()
