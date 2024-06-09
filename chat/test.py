import requests

url = "https://token.oaifree.com/api/auth/refresh"
headers = {
    "Content-Type": " x-www-form-urlencoded;charset=UTF-8"
}
data = {
    "refresh_token": ""
}
response = requests.post(url, data=data)
print(response.json()["access_token"])
