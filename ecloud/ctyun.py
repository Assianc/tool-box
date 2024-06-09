import requests
import hashlib
import time
from environs import Env


def keep_alive(ctyun, retries=3, delay=10):
    # 设置API的URL和路径
    url = "https://desk.ctyun.cn:8810/api/"
    computer_connect = "desktop/client/connect"

    # 设置连接云电脑时需要的设备信息
    device_info = {
        "objId": ctyun["objId"],
        "objType": 0,
        "osType": 15,
        "deviceId": 60,
        "deviceCode": ctyun["deviceCode"],
        "deviceName": "Edge浏览器",
        "sysVersion": "Windows NT 10.0; Win64; x64",
        "appVersion": "1.36.1",
        "hostName": "Edge浏览器",
        "vdCommand": "",
        "ipAddress": "",
        "macAddress": "",
        "hardwareFeatureCode": ctyun["deviceCode"]
    }

    # 配置请求头中需要的一些参数
    app_model_value = "2"
    device_code_value = ctyun["deviceCode"]
    device_type_value = "60"
    request_id_value = "1704522993726"
    tenant_id_value = "15"
    timestamp_value = str(int(time.time() * 1000))
    userid_value = ctyun["userid"]
    version_value = "201360101"
    secret_key_value = ctyun["secret_key"]

    # 创建签名字符串
    signature_str = device_type_value + request_id_value + tenant_id_value + timestamp_value + userid_value + version_value + secret_key_value

    # 使用MD5算法创建签名
    hash_obj = hashlib.md5()
    hash_obj.update(signature_str.encode('utf-8'))
    digest_hex = hash_obj.hexdigest().upper()

    # 准备请求头
    headers = {
        'ctg-appmodel': app_model_value,
        'ctg-devicecode': device_code_value,
        'ctg-devicetype': device_type_value,
        'ctg-requestid': request_id_value,
        'ctg-signaturestr': digest_hex,
        'ctg-tenantid': tenant_id_value,
        'ctg-timestamp': timestamp_value,
        'ctg-userid': userid_value,
        'ctg-version': version_value
    }

    # 发起POST请求连接云电脑
    for attempt in range(retries):
        try:
            response = requests.post(url + computer_connect, data=device_info, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectTimeout:
            if attempt < retries - 1:
                time.sleep(delay)
                continue
            else:
                raise "连接超时"


def cf_worker(message, method="qywx", api_type="default", msgtype="text", worker_url="https://qyapi.bxin.top/msg",
              webhook=None):
    # 构建POST请求的数据
    data = {
        "method": method,
        "content": {
            "type": api_type,
            "msgtype": msgtype,
            "message": message,
            "webhook": webhook,
        },
    }

    # 发送POST请求到Cloudflare Worker
    response = requests.post(worker_url, json=data)

    print(response.text)


def main():
    env = Env()
    env.read_env()
    ctyuns = env.json("CTYUN")
    for ctyun in ctyuns:
        try:
            data = keep_alive(ctyun)
            code = data["code"]
            if code == 0:
                # cf_worker(f"{ctyun['objId']} 保活成功")
                pass
            else:
                cf_worker(f"保活失败：{data}")
        except Exception as e:
            cf_worker(f"保活失败：{e}")


if __name__ == '__main__':
    main()
