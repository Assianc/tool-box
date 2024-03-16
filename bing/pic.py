import requests
import urllib.parse
import os
from dotenv import load_dotenv


def get_daily_image():
    daily_image_url = 'https://global.bing.com/HPImageArchive.aspx?format=js&idx=0&n=9&pid=hp&FORM=BEHPTB&uhd=1&uhdwidth=3840&uhdheight=2160&setmkt=zh_cn&setlang=zh'
    try:
        r = requests.get(daily_image_url)
        r = r.json()
        return 'https://global.bing.com/' + r['images'][0]['url']
    except Exception as e:
        print(f'bing获取壁纸失败：{e}')


class ImageDriver:
    def __init__(self, driver='bing'):
        self.driver = driver

    def get_image_url(self):
        if self.driver == 'bing':
            return get_daily_image()
        return None


if __name__ == '__main__':
    # 读取.env文件中的变量
    load_dotenv()
    try:
        driver = os.environ['DRIVER']  # bing
    except Exception as e:
        print(f'获取DRIVER失败：{e}')
        driver = 'bing'

    image_driver = ImageDriver(driver)
    image_url = image_driver.get_image_url()
    # https://global.bing.com//th?id=OHR.BambooPanda_ZH-CN8455481760_UHD.jpg&rf=LaDigue_UHD.jpg&pid=hp&w=3840&h=2160&rs=1&c=4
    # 下载图片，保存到当前目录下的images文件夹，文件名为链接上的id
    if image_url:
        image_id = image_url.split('id=')[1].split('_')[0]
        image_path = f'images/{image_id}.jpg'
        if not os.path.exists(image_path):
            urllib.request.urlretrieve(image_url, image_path)
            print(f'壁纸下载成功：{image_path}')
        else:
            print(f'壁纸已存在：{image_path}')
    else:
        print('获取壁纸失败')
