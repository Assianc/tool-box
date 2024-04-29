import os
import random
import smtplib
import string
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3
from apyori import apriori
from dotenv import load_dotenv


def apriori_analysis(random_string):
    try:
        with open('./also_bought.txt', "r") as f:
            content = f.read()
    except:
        # GitHub Action
        with open('socialNetworking/also_bought.txt', "r") as f:
            content = f.read()

    lines = content.splitlines()

    data = [eval(line) for line in lines]

    # 调用 apriori 函数计算关联规则
    items = apriori(data, min_support=10 / len(data))

    items_list = list(items)

    with open(f"socialnet_{random_string}.csv", "w") as file:
        file.write(str(items_list))


def cf_r2(random_string):
    load_dotenv()
    ACCOUNT_ID = os.environ['ACCOUNT_ID']
    ACCESS_KEY_ID = os.environ['ACCESS_KEY_ID']
    SECRET_ACCESS_KEY = os.environ['SECRET_ACCESS_KEY']

    # 创建 S3 客户端
    s3 = boto3.client(
        's3',
        region_name='auto',
        endpoint_url=f'https://{ACCOUNT_ID}.r2.cloudflarestorage.com',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY
    )

    # 上传文件
    object_key = f'socialnet_{random_string}.csv'
    file_path = object_key
    bucket_name = 'cloud'

    with open(file_path, 'rb') as file:
        s3.upload_fileobj(
            Fileobj=file,
            Bucket=bucket_name,
            Key=f'social/{object_key}'
        )

    print(f'https://cloud.bxin.top/social/{object_key}')


def send_email(random_string):
    load_dotenv()
    # 电子邮件配置
    sender_email = os.environ['SENDER_EMAIL']
    sender_password = os.environ['SENDER_PASSWORD']
    receiver_emails = ['social@bxin.top']

    article_content = f"关联规则"

    # 创建MIMEText对象
    msg = MIMEMultipart()
    msg.attach(MIMEText(article_content, 'plain'))
    # 设置发件人和收件人
    msg['From'] = sender_email
    msg['Subject'] = f'关联规则'

    # 添加附件
    filename = f"socialnet_{random_string}.csv"
    attachment = open(filename, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {filename}")
    msg.attach(part)

    # 连接到SMTP服务器并发送邮件
    with smtplib.SMTP_SSL('smtp.163.com', 465) as server:
        server.login(sender_email, sender_password)
        for receiver_email in receiver_emails:
            msg['To'] = receiver_email
            server.sendmail(sender_email, receiver_email, msg.as_string())


def main():
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    apriori_analysis(random_string)

    # 文件接收方式,二选一
    try:
        cf_r2(random_string)
        send_email(random_string)
    except:
        pass


if __name__ == '__main__':
    main()
