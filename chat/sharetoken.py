import requests
import random
import time

refresh_token = ''


# 获取当前时间戳
def get_current_timestamp():
    return int(time.time())


# 使用 rt 换取 at
def get_access_token(refresh_token):
    url = 'https://token.oaifree.com/api/auth/refresh'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'refresh_token': refresh_token}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        data = response.json()
        if 'access_token' in data:
            return data['access_token']
        else:
            raise Exception('Failed to generate access token, response: ' + str(data))
    else:
        raise Exception('Failed to refresh access token')


# 使用 at 生成 st
def get_share_token(access_token):
    url = 'https://chat.oaifree.com/token/register'
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    data = {
        'unique_name': generate_random_hex(8),
        'access_token': access_token,
        'expires_in': 0,
        'site_limit': '',
        'gpt35_limit': -1,
        'gpt4_limit': -1,
        "temporary_chat": True,
        'show_conversations': True
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        data = response.json()
        expire_at = data.get('expire_at')
        if expire_at:
            return data['token_key'], expire_at
        else:
            raise Exception('Failed to generate share token, response: ' + str(data))
    else:
        raise Exception('Failed to generate share token')


# 生成随机字符串
def generate_random_hex(length):
    characters = '0123456789abcdef'
    return ''.join(random.choice(characters) for _ in range(length))


# 自动登录
def auto_login(share_token):
    login_url = f'https://chat.xbxin.com/auth/login_share?token={share_token}'
    print('Logging in with URL:', login_url)
    # 实际应用中可能需要使用浏览器打开登录链接


# 检查 st 是否过期
def is_st_expired(expire_at):
    return get_current_timestamp() >= expire_at


def main():
    try:
        share_token = None
        share_token_expire = 0

        if share_token_expire == 0:
            print('Initializing share token...')
            access_token = get_access_token(refresh_token)
            share_token, expire_at = get_share_token(access_token)
            print('Share token initialized:', share_token)
            print('Share token expiration:', expire_at)
        else:
            print('Share token already initialized.')

        if is_st_expired(expire_at):
            print('ST token is expired. Refreshing tokens...')
            access_token = get_access_token(refresh_token)
            print('Access token obtained:', access_token)
            share_token, expire_at = get_share_token(access_token)
            print('Share token refreshed:', share_token)
            print('Share token expiration:', expire_at)
        else:
            print('ST token is still valid.')

        auto_login(share_token)
    except Exception as e:
        print('Error:', e)


if __name__ == '__main__':
    main()
