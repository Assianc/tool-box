import requests
from environs import Env

env = Env()
env.read_env()

API_TOKEN = env.str("CF_AI_TOKEN")
API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/979949db46ca518e090a23bff4f681eb/ai/run/"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def run(model, inputs):
    input = {"messages": inputs}
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    return response.json()


inputs = [
    {"role": "system", "content": "You are a friendly assistan that helps write stories"},
    {"role": "user", "content": "你会使用中文吗"}
];
output = run("@cf/baai/bge-small-en-v1.5", inputs)
print(output)
