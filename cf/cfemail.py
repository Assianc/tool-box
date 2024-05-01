import requests


def send_cf_email(subject, body, to_email, from_email, method="cfemail", worker_url="https://qyapi.bxin.top/msg"):
    data = {
        "method": method,
        "content": {
            "subject": subject,
            "body": body,
            "to_email": to_email,
            "from_email": from_email
        }
    }
    response = requests.post(worker_url, json=data)

    print(response.text)


def main():
    # send_cf_email("test", "test", "test@bxin.top", "bxin@bxin.top")
    send_cf_email("test", "test", "testto@bxin.top", "testfrom@bxin.top", worker_url="http://127.0.0.1:8787/msg")


if __name__ == '__main__':
    main()
