import requests
from settings import OPENAI_API_KEY, OPENAI_URL, OPENAI_MODEL, OPENAI_HOST, OPENAI_API_VERSION, PROXY_URL


def query_chatgpt(prompt):
    proxies = {'https': PROXY_URL}
    params = {'api-version': OPENAI_API_VERSION}
    payload = {'model': OPENAI_MODEL,
               'messages': [{'role': 'user', 'content': prompt}]}
    headers = {
        'api-key': OPENAI_API_KEY,
        'Content-Type': 'application/json',
        'User-Agent': 'PostmanRuntime/7.31.1',
        'Accept': '*/*',
        'Host': OPENAI_HOST,
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Content-Length': str(len(prompt)),
    }

    response = requests.post(OPENAI_URL, params=params, headers=headers, json=payload, proxies=proxies, verify=False)
    response = response.json()

    return response['choices'][0]['message']['content']
