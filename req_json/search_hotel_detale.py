from loguru import logger
from req_json.api_request import api_request


def hotel_detale(hotel_id: str, foto_num: int = 1) -> list:
    """
    Функция поиска детальной информации по отелю
    :param hotel_id:
    :param foto_num:
    :return:
    """
    logger.info(f'Пользователь выполнил команду "hotel_detale"')
    params = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": hotel_id
    }

    data = api_request(method_endswith='properties/v2/detail', params=params, method_type="POST")

    address = data["data"]["propertyInfo"]['summary']['location']['address']['addressLine']
    hotel_foto = [data["data"]["propertyInfo"]['propertyGallery']['images'][i]['image']['url'] for i in range(foto_num)]
    return [address, hotel_foto]