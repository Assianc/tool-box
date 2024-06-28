import requests
from environs import Env


def get_models(base_url, api_key):
    if base_url == 'https://gptgod.online':
        url = f'{base_url}/api/user/info'
    elif base_url == 'http://api.aicnn.cn':
        return []
    else:
        url = f'{base_url}/v1/models'

    headers = {
        'authorization': f'Bearer {api_key}',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/126.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        models = parse_models(response.json())
        return models
    except Exception as e:
        print(e)
        return []


def parse_models(data):
    data = data['data']

    models = []

    # 判断data下是否有键models
    if 'models' in data:
        data = data['models']
        for item in data:
            models.append(item['model'])
    else:
        for item in data:
            models.append(item['id'])
    return models


def main():
    env = Env()
    env.read_env()
    api_list = env.json('ONE_API')

    models = set()
    id = 0
    for api in api_list[id:id + 1]:
        print(api['base_url'])
        model_list = get_models(api['base_url'], api['api_key'])
        for model in model_list:
            if model not in models:
                models.add(model)

    models = sorted(models)

    base_models = "-all"

    for model in models:
        base_models += ",+" + model

    print(base_models)


if __name__ == '__main__':
    main()
