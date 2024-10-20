import requests
from Config import config
from loguru import logger
import time


def api_request(method_endswith,  # Меняется в зависимости от запроса. locations/v3/search либо properties/v2/list
                params,  # Параметры, если locations/v3/search, то {'q': 'Рига', 'locale': 'ru_RU'}
                method_type  # Метод\тип запроса GET\POST
                ):
    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"

    if method_type == 'GET':
        return get_request(
            url=url,
            params=params
        )
    else:
        return post_request(
            url=url,
            params=params
        )


def get_request(url, params):
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    for i in range(1, 4):
        try:
            response = requests.request("GET", url, headers=headers, params=params, timeout=15)
            if response.status_code == requests.codes.ok:
                return response.json()
        except Exception:
            logger.error(f'Ошибка соединения get_request #{i}')
            time.sleep(2)
    return None


def post_request(url, params):
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    try:
        response = requests.request("POST", url, headers=headers, json=params, timeout=10)
        if response.status_code == requests.codes.ok:
            return response.json()
    except Exception:
        logger.error(f'Ошибка соединения post_request')