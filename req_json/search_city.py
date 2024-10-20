from loguru import logger
from req_json.api_request import api_request


def search_city(city: str):
    logger.info(f'Пользователь выполнил команду "search_city"')
    params = {
        "q": city,
        "locale": "en_US",
        "langid": "1033",
        "siteid": "300000001"
    }
    data = api_request(method_endswith='locations/v3/search', params=params, method_type="GET")

    if data is None:
        logger.error('Ошибка соединения!')
        return False
    if not data['sr']:
        logger.error('Нет такого города!')
        return False
    result = {i_city["essId"]["sourceId"]: i_city["regionNames"]["displayName"] for i_city in data['sr']}
    return result
