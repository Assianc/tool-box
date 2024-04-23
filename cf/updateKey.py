import requests


def update_key_value(api_token, account_id, namespace_id, key, new_value):
    # API URL
    url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/{key}'

    # 请求头
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'Content-Type:application/json',
    }

    # 发送请求
    response = requests.put(url, headers=headers, data=new_value)

    if response.status_code == 200:
        print("键值对更新成功！")
    else:
        print("更新失败：", response.text)


# 你的 API 信息
api_token = 'hGxxxxxxxxxxxxxxxxx'
account_id = 'bcxxxxxxxxxxxxxxxxxx'
zone_id = '95axxxxxxxxxxxxxxxxxxxxxxxxxxx'
namespace_id = '2bxxxxxxxxxxxxxxxxxx'
key = 'at'  # 要修改的键
new_value = 'new_value'  # 新的值

update_key_value(api_token, account_id, namespace_id, key, new_value)