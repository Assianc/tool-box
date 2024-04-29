import os

import boto3
from dotenv import load_dotenv

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
object_key = 'apriori.csv'
file_path = f'./{object_key}'
bucket_name = 'cloud'

with open(file_path, 'rb') as file:
    response = s3.upload_fileobj(
        Fileobj=file,
        Bucket=bucket_name,
        Key=f'social/{object_key}'
    )

print(f'https://cloud.bxin.top/{object_key}')
