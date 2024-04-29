import os
import random
import string

import boto3
from apyori import apriori
from dotenv import load_dotenv


def apriori_analysis(random_string):
    file_path = "also_bought.txt"
    # 读取数据
    with open(file_path, "r") as f:
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


def main():
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    apriori_analysis(random_string)
    cf_r2(random_string)


if __name__ == '__main__':
    main()
