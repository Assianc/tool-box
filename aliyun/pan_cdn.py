import base64
import json
import time

import requests
from crypto_plus import CryptoPlus
from flask import Flask, request

rsa = CryptoPlus.loads('''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC72/8TD242+vn0FDQm8YyeY2WH
rNIxpiCgGT6H5EbDgo7mAXy5+LtJ/imCrqfYli4mwW3SPagtGlTo1OrlqafX+pIs
ehYnKuMQEW9nPbJ0z3ItrFx1cTC70Dx3mk6mrK+KOx6XgfiLqrgGy/wysbPX5PdN
Apg4Wc3GsMk8UpdtGQIDAQAB
-----END PUBLIC KEY-----''')


def is_expired(access_token):
    if not access_token:
        return True
    try:
        message, signature = access_token.rsplit('.', 1)
        header, payload = message.split('.')
        payload = payload + '=' * - (len(payload) % - 4)
        signature = signature + '=' * - (len(signature) % - 4)
        exp = json.loads(base64.b64decode(payload).decode()).get('exp')
        return exp - time.time() < 10 or not rsa.verify(message.encode(), base64.urlsafe_b64decode(signature))
    except:
        return True


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def download_url_form():
    if request.method == 'POST':
        file_id = request.form['file_id']
        access_token = request.form['access_token']
        if is_expired(access_token):
            return 'token is expired', 401

        drive_info = requests.post('https://bj29.api.aliyunpds.com/v2/drive/list_my_drives', json={
        }, headers={
            "Authorization": f"Bearer {access_token}",
        }).json()
        driver_id_map = {i['category']: i['drive_id'] for i in drive_info['items'] if
                         i['category'] in ['backup', 'resource']}
        resp = requests.post('https://bj29.api.aliyunpds.com/v2/file/get_download_url', json={
            'drive_id': driver_id_map['resource'],
            'file_id': file_id,
            'expire_sec': 115200,
        }, headers={
            'Authorization': f'Bearer {access_token}',
        })
        if resp.status_code == 404:
            resp = requests.post('https://bj29.api.aliyunpds.com/v2/file/get_download_url', json={
                'drive_id': driver_id_map['backup'],
                'file_id': file_id,
                'expire_sec': 115200,
            }, headers={
                'Authorization': f'Bearer {access_token}',
            })
        if resp.status_code == 200:
            data = resp.json()
            url = data.get('cdn_url')
            if not url:
                url = data.get('url')
            return f'<h1>Download URL:</h1><p>{url}</p>'
        return f'<h1>Error:</h1><p>{resp.reason}</p>'

    # 如果是 GET 请求，渲染表单
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Download URL Form</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f0f0;
                }
                .container {
                    max-width: 400px;
                    margin: 50px auto;
                    padding: 20px;
                    background-color: #fff;
                    border-radius: 5px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    font-size: 24px;
                    margin-bottom: 20px;
                    text-align: center;
                }
                form {
                    display: flex;
                    flex-direction: column;
                }
                label {
                    font-size: 16px;
                    margin-bottom: 8px;
                }
                input[type="text"] {
                    padding: 10px;
                    margin-bottom: 20px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    font-size: 16px;
                }
                button {
                    padding: 10px;
                    background-color: #007bff;
                    color: #fff;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Download URL Form</h1>
                <form action="/" method="post">
                    <label for="file_id">File ID:</label>
                    <input type="text" id="file_id" name="file_id" required>
                    <label for="access_token">Access Token:</label>
                    <input type="text" id="access_token" name="access_token" required>
                    <button type="submit">Get Download URL</button>
                </form>
            </div>
        </body>
        </html>
    '''


if __name__ == '__main__':
    app.run()