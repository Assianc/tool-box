import requests
import json
import urllib.parse
import datetime
import random
import os
from dotenv import dotenv_values
import warnings

warnings.filterwarnings("ignore")


class Alist:
    domain = None
    usernaem = None
    password = None
    base_path = None
    token = None

    def __init__(self, domain, username, password, base_path, namespace=None):
        self.domain = domain
        self.username = username
        self.password = password
        self.base_path = base_path
        if namespace:
            self.base_path = self.base_path + '/' + namespace
        self.init_token()
        pass

    def init_token(self):
        try:
            url = self.domain + '/api/auth/login'
            payload = json.dumps({
                "username": self.username,
                "password": self.password
            })
            headers = {
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            print('获取token结果：', response.text)
            if response.status_code != 200:
                raise response.text
            data = response.json()
            if data['code'] != 200:
                print(data['message'])
                return
            self.token = data['data']['token']
        except Exception as e:
            print(f'获取token失败：{e}')

    def check_token(self):
        if self.token is None:
            raise 'token获取失败，上传失败'
        pass

    def upload_file(self, file_path=None, target_path=None, bytes=None):
        try:
            self.check_token()
            url = self.domain + "/api/fs/put"
            # 读取文件内容
            payload = bytes
            if payload is None:
                with open(file_path, 'rb') as f:
                    payload = f.read()  # 二进制文件内容

            if payload is None:
                print('文件内容为空，上传失败')
                return None
            # payload="<file contents here>"
            file_helper: FileHelper = FileHelper()
            headers = {
                'Authorization': self.token,
                'File-Path': file_helper.encode_file_path(self.base_path + '/' + target_path),
                'As-Task': 'true',
                'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
                'Content-Type': 'text/plain'
            }

            response = requests.request("PUT", url, headers=headers, data=payload)

            print('上传结果：', response.text)
            json_data = response.json()
            if json_data['code'] == 200:
                print("上传成功！！")
                return True
            return False
        except Exception as e:
            print(f'上传文件失败：{e}')
            return False


class FileHelper:

    def __init__(self):
        pass

    def encode_file_path(self, file_path):
        # 替换反斜杠为正斜杠
        file_path = file_path.replace('\\', '/')
        # URL编码
        encoded_path = urllib.parse.quote(file_path)
        return encoded_path

    def parse_url_file_prefix(self, url):
        # 不区分大小写
        url = url.lower()
        if 'jpg' in url:
            return '.jpg'
        if 'png' in url:
            return '.png'
        if 'jpeg' in url:
            return '.jpeg'
        return '.jpg'

    # 生成随机字符串
    def random_str(self, random_num=8):
        str = ''
        number_chars = '0123456789'
        for i in range(random_num):
            str += random.choice(number_chars)
        return str

    # 生成无符号时间+随机数文件名称
    def gen_file_name(self, url):
        now = datetime.datetime.now()
        file_name = now.strftime("%Y%m%d%H%M%S") + '_' + self.random_str() + self.parse_url_file_prefix(url)
        return file_name

    def download_bytes(self, url):
        # 下载文件
        response = requests.get(url, verify=False, stream=True)
        return response.content


class BingDriver:
    daily_image_url = 'https://global.bing.com/HPImageArchive.aspx?format=js&idx=0&n=9&pid=hp&FORM=BEHPTB&uhd=1&uhdwidth=3840&uhdheight=2160&setmkt=zh_cn&setlang=zh'

    def __init__(self):
        pass

    def get_daily_image(self):
        try:
            r = requests.get(self.daily_image_url)
            r = r.json()
            return 'https://global.bing.com/' + r['images'][0]['url']
        except Exception as e:
            print(f'bing获取壁纸失败：{e}')
            pass


class ImageDriver:
    driver = None

    def __init__(self, driver):
        self.driver = driver
        pass

    def get_image_url(self):
        if self.driver == 'bing':
            bing_driver = BingDriver()
            return bing_driver.get_daily_image()
        return None


if __name__ == '__main__':
    # 读取.env文件中的变量
    env = dotenv_values(os.path.dirname(__file__) + "/.env")
    domain = env.get('DOMAIN')
    username = env.get('USERNAME')
    password = env.get('PASSWORD')
    base_path = env.get('BASE_PATH')
    namespace = env.get('NAMESPACE')
    driver = env.get('DRIVER')  # bing

    if domain is None:
        print('请先配置domain')
        exit(1)
    if username is None:
        print('请先配置username')
        exit(1)
    if password is None:
        print('请先配置password')
        exit(1)
    if base_path is None:
        print('请先配置base_path')
        exit(1)

    if driver is None:
        # 默认为bing
        driver = 'bing'

    alist: Alist = Alist(domain=domain, username=username, password=password, base_path=base_path, namespace=namespace)

    image_driver: ImageDriver = ImageDriver(driver)
    image_url = image_driver.get_image_url()

    file_helper: FileHelper = FileHelper()
    bytes = file_helper.download_bytes(image_url)

    # 从URL中获取后缀生成文件名
    file_name = file_helper.gen_file_name(image_url)
    now = datetime.datetime.now()
    alist.upload_file(target_path=f'{now.strftime("%Y%m%d")}/{file_name}', bytes=bytes)