import os
import traceback

import requests
from environs import Env


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
def get_dns_records(name, cf, ):
    headers = {
        'Authorization': f'Bearer {cf["API_TOKEN"]}',
        'Content-Type': 'application/json'
    }

    def_info = []
    url = f'https://api.cloudflare.com/client/v4/zones/{cf["ZONE_ID"]}/dns_records'
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
def update_dns_record(record_id, name, cf_ip, cf):
    headers = {
        'Authorization': f'Bearer {cf["API_TOKEN"]}',
        'Content-Type': 'application/json'
    }

    url = f'https://api.cloudflare.com/client/v4/zones/{cf["ZONE_ID"]}/dns_records/{record_id}'
    data = {
        'type': 'A',
        'name': name,
        'content': cf_ip
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        return '解析成功'
    else:
        data = response.json()
        error_msg = data['errors'][0]['message']
        if error_msg == 'Record already exists.':
            return '解析已存在'
        else:
            traceback.print_exc()
            return f"ip {cf_ip} 解析失败：{response.text}"


def cf_msg(message, method="qywx", webhook="H", type="text", worker_url="https://api.xbxin.com/msg", ):
    data = {
        "method": method,
        "content": {
            "webhook": webhook,
            "type": type,
            "message": message,
        },
    }

    requests.post(worker_url, json=data)


# 主函数
def main():
    # 读取环境变量
    env = Env()
    env.read_env()
    CF = env.json("CF")
    CF_DNS_NAME = env.str("CF_DNS_NAME")

    # 获取最新优选IP
    ip_addresses_str = get_cf_speed_test_ip()
    ip_addresses = ip_addresses_str.split(',')

    for i in range(len(CF)):
        dns_records = get_dns_records(CF_DNS_NAME, CF[i])
        content = f''

        # 遍历 IP 地址列表
        for index, ip_address in enumerate(ip_addresses):
            # 执行 DNS 变更
            dns = update_dns_record(dns_records[index], CF_DNS_NAME, ip_address, CF[i])
            if dns.startswith('ip'):
                content += f'{dns}\n'

        if content:
            cf_msg(content)


if __name__ == '__main__':
    main()
