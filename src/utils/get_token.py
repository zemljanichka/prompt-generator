from datetime import timedelta
from cachetools import cached, TTLCache
import requests
import os

def get_token(auth_key):
    url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
    api_token = requests.post(url=url, json={"yandexPassportOauthToken": auth_key})
    return(api_token.json())

@cached(TTLCache(maxsize=128, ttl=timedelta(hours=3).total_seconds()))
def get_yandex_token() -> str:
    auth_key = os.environ.get("AUTH_KEY_YANDEXGPT")
    new_token = get_token(auth_key)
    if 'iamToken' in new_token:
        print(f" Updated API_KEY_YANDEXGPT to: {new_token['iamToken']}")
        return new_token['iamToken']            
    else:
        raise ValueError('Token not found')
    