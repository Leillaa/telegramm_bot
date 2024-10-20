from loader import bot
from loguru import logger
from Database.sqlite_db_loader import user_history
from aiogram import Dispatcher, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
from Keyboards.inline_kb import inline_keyboard_help
from Handlers.func import delete_message, show_hotel_info


async def show_hotel(callback: CallbackQuery) -> None:
    await delete_message(callback)
    i_req = callback.data.split('_')
    """
    i_req[0] = 'hist_'
    i_req[1] = history request (1, 2, ...)
    i_req[2] = user_id
    """
    hotel_history_dict = user_history(i_req[2])[int(i_req[1])]
    for i_hotel in hotel_history_dict['hotels'].values():
        await show_hotel_info(int(i_req[2]), i_hotel)


async def history(message: Message) -> None:
    """
    Ответ на команду history
    :param message:
    :return:
    """
    await delete_message(message)
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) выполнил команду "history"')
    user_history_list = user_history(message.from_user.id)
    req_type = {
        'lowprice': 'низкая цена',
        'highprice': 'высокая цена',
        'custom': 'подбор значений'
    }
    if user_history_list:
        await bot.send_message(message.from_user.id,
                               f'Твоя история запросов, {message.from_user.full_name}:',
                               reply_markup=types.ReplyKeyboardRemove())
        for i_code, i_value in user_history_list.items():
            text = f'Дата и время запроса: {i_value["time"]}\n' \
                   f'Тип запроса: {req_type[i_value["request"]]}\n' \
                   f'Город: {i_value["city"]}\n' \
                   f'Отелей найдено: {i_value["hotel_num"]} '
            i_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Просмотреть',
                                                                   callback_data='hist_' + str(i_code) + '_' +
                                                                                 str(message.from_user.id)))
            await bot.send_message(message.from_user.id, text, reply_markup=i_kb)
    else:
        await bot.send_message(message.from_user.id,
                               f'{message.from_user.full_name}, твоя история запросов пуста!',
                               reply_markup=inline_keyboard_help())


def register_user_handlers(disp: Dispatcher) -> None:
    """
    Резистрирует message_handler и callback_query_handler для функций
    :param disp:
    :return:
    """
    disp.register_message_handler(history, commands=['history'])
    disp.register_callback_query_handler(history, text=['/history'])
    disp.register_callback_query_handler(show_hotel, Text(startswith='hist_'))
