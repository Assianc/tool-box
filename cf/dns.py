import json

import requests
import traceback
import os
from dotenv import load_dotenv

load_dotenv()
# API 密钥
CF_API_TOKEN = os.environ["CF_API_TOKEN"]
CF_ZONE_ID = os.environ["CF_ZONE_ID"]
CF_DNS_NAME = os.environ["CF_DNS_NAME"]

headers = {
    'Authorization': f'Bearer {CF_API_TOKEN}',
    'Content-Type': 'application/json'
}


def get_cf_speed_test_ip(timeout=10, max_retries=5):
    for attempt in range(max_retries):
        try:
            # 发送 GET 请求，设置超时
            response = requests.get('https://ip.164746.xyz/ipTop.html', timeout=timeout)
            # 检查响应状态码
            if response.status_code == 200:
                return response.text
        except Exception as e:
            traceback.print_exc()
            print(f"get_cf_speed_test_ip Request failed (attempt {attempt + 1}/{max_retries}): {e}")
    return None


# 获取 DNS 记录
def get_dns_records(name):
    def_info = []
    url = f'https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        records = response.json()['result']
        for record in records:
            if record['name'] == name:
                def_info.append(record['id'])
        return def_info
    else:
        print('Error fetching DNS records:', response.text)


# 更新 DNS 记录
def update_dns_record(record_id, name, cf_ip):
    url = f'https://api.cloudflare.com/client/v4/zones/{CF_ZONE_ID}/dns_records/{record_id}'
    data = {
        'type': 'A',
        'name': name,
        'content': cf_ip
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        return '解析成功'
    else:
        traceback.print_exc()
        return f"ip {cf_ip} 解析失败：{response.text}"


# 主函数
def main():
    # 获取最新优选IP
    ip_addresses_str = get_cf_speed_test_ip()
    ip_addresses = ip_addresses_str.split(',')
    dns_records = get_dns_records(CF_DNS_NAME)
    content = f''

    # 遍历 IP 地址列表
    for index, ip_address in enumerate(ip_addresses):
        # 执行 DNS 变更
        dns = update_dns_record(dns_records[index], CF_DNS_NAME, ip_address)
        if dns.startswith('ip'):
            content += f'{dns}\n'

    if content:
        cf_worker(content)


def cf_worker(message, method='qywx', api_type='default', worker_url='https://qyapi.bxin.top/msg'):
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


if __name__ == '__main__':
    main()
