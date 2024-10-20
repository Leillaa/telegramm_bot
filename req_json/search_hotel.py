from req_json.search_hotel_detale import hotel_detale
from req_json.api_request import api_request
from loguru import logger
from Handlers.func import show_hotel_info
from loader import bot


async def s_hotel(chat_id: str, city_id: str, hotel_num: int, foto: bool, req: str, min_cust: None, max_cust: None) -> dict or None:
    """
    Функция поиска отелей в выбранном городе
    :param max_cust:
    :param min_cust:
    :param req:
    :param foto:
    :param hotel_num:
    :param chat_id:
    :param city_id:
    :return:
    """
    logger.info(f'Пользователь выполнил команду "s_hotel"')
    params = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": city_id},
        "checkInDate": {
            "day": 10,
            "month": 10,
            "year": 2022
        },
        "checkOutDate": {
            "day": 15,
            "month": 10,
            "year": 2022
        },
        "rooms": [
            {
                "adults": 2,
                "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {"price": {
            "max": 150,
            "min": 100
        }}
    }

    data = api_request(method_endswith='properties/v2/list', params=params, method_type="POST")

    if data['data']:
        hotels_list = data["data"]["propertySearch"]['properties']
        result = {}
        min_price = hotels_list[0]['price']['lead']['formatted']
        max_price = hotels_list[-1]['price']['lead']['formatted']
        await bot.send_message(chat_id, f'Всего в выбранном городе найдено отелей: {len(hotels_list)}\n'
                                        f'Цены: от {min_price} до {max_price}')
        for i_hotel in hotels_list:

            result[i_hotel["id"]] = {
                'name': i_hotel["name"],
                'price': i_hotel['price']['lead']['amount'],
                'f_price': i_hotel['price']['lead']['formatted'],

                'link': f"https://www.hotels.com/h{i_hotel['id']}.Hotel-Information"
            }

        # на тот случай, если отелей в городе меньше, чем было в запросе
        i_num_hotel = 1
        result_num = {}

        # сортировка словаря с отелями
        if req == 'lowprice':
            result_sorted = dict(sorted(result.items(), key=lambda x: x[1].get('price')))
        elif req == 'highprice':
            result_sorted = dict(sorted(result.items(), key=lambda x: x[1].get('price'), reverse=True))
        else:
            filtered_hotels = filter(lambda hotel: min_cust <= hotel['price']['lead']['amount'] <= max_cust, hotels_list)
            result_sorted = {}
            for hotel in filtered_hotels:
                result_sorted[hotel["id"]] = {
                    'name': hotel["name"],
                    'price': hotel['price']['lead']['amount'],
                    'f_price': hotel['price']['lead']['formatted'],

                    'link': f"https://www.hotels.com/h{hotel['id']}.Hotel-Information"
                }
        print(result_sorted)
        for i_code, i_hotel in result_sorted.items():
            if i_num_hotel > hotel_num:
                return result_num
            result_num[i_code] = i_hotel
            address, hotel_foto = hotel_detale(i_code)
            result_num[i_code]['address'] = address
            if foto:
                result_num[i_code]['hotel_foto'] = hotel_foto
            else:
                result_num[i_code]['hotel_foto'] = []
            await show_hotel_info(chat_id, result_num[i_code])
            i_num_hotel += 1
        return result_num
    else:
        return None
