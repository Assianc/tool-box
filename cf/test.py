import requests

data = {
    "from": "sender@bxin.top",
    "fromn": "Sender Name",
    "to": "receiver@bxin.top",
    "ton": "Receiver Name",
    "rep": "",
    "repn": "",
    "dkim": "",
    "dkims": "",
    "dkimpk": "",
    "type": "text/plain; charset=utf-8",
    "sbj": "Email Subject",
    "body": "Email Body"
}

response = requests.post('https://email.bxin.workers.dev/', data=data)

print(response.text)
