import requests

json_data = {
    'name': 'paula18',
    'domain': 'xbxin.com',
    'cf_token': '',
}

# response = requests.post('https://email-api.xbxin.com/api/new_address', json=json_data)
response = requests.post('http://127.0.0.1:8787/api/new_address', json=json_data)
print(response)
