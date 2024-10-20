from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from states.request_info import FSMCustom
from loguru import logger
from loader import bot
from typing import Union
from Keyboards.reply_kb import kb_yn, kb_foto_num, kb_reply_cancel
from Keyboards.inline_kb import kb_cities, inline_keyboard_help
from Database.sqlite_db_loader import request_add, user_add
from req_json import search_city, search_hotel
from Handlers.func import delete_message, cancel_handler


async def start_fsm(message: Union[Message, CallbackQuery]) -> None:
    """
    Начало диалога. Ввод названия города
    :param message:
    :return:
    """
    await delete_message(message)
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) выполнил команду "Custom"')
    await bot.send_message(message.from_user.id, 'Введите название города', reply_markup=kb_reply_cancel)
    await FSMCustom.step_1.set()


async def step_city(message: types.Message, state: FSMContext) -> None:
    """
    Выбот ответа из  списка и запись его в словарь
    :param message:
    :param state:
    :return:
    """
    logger.info(f'Custom Пользователь {message.from_user.full_name}({message.from_user.id}) в функции load_dif_city!')
    rezult = search_city.search_city(message.text)
    if rezult:
        async with state.proxy() as data:
            data['city_dict'] = rezult

        await bot.send_message(message.from_user.id, 'Уточните метоположение', reply_markup=kb_cities(rezult))
        await FSMCustom.next()
    else:
        await bot.send_message(message.from_user.id, 'Такого города не обнаружено или произошла ошибка соединения, '
                                                     'повторите ввод или наберите "отмена"',
                               reply_markup=kb_reply_cancel)
        logger.debug(f'Пользователь {message.from_user.full_name}({message.from_user.id}) '
                     f'- Ошибка ввода названия города')


async def step_not_city(message: types.Message):
    """
    Удаление сообщений если нет колбека
    :param message:
    :return:
    """
    await message.delete()


async def step_load_city(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Запись ответа пользователя в словарь и вывод вопроса о количетве отелей
    :param callback:
    :param state:
    :return:
    """
    logger.info(f'lowprice Пользователь в функции load_city!')
    await delete_message(callback)
    if callback.data == 'cancel':
        await cancel_handler(callback.message, state)
    else:
        async with state.proxy() as data:
            data['city'] = callback.data
        await callback.message.answer('Введите количество отелей (от 1 до 10)', reply_markup=kb_foto_num)
        await FSMCustom.next()


async def step_hotel_num(message: types.Message, state: FSMContext) -> None:
    """
    Запись ответа от пользователя в словарь и вывод вопроса о фото отелей
    :param message:
    :param state:
    :return:
    """
    logger.info(f'Custom Пользователь {message.from_user.full_name}({message.from_user.id}) '
                f'в функции load_hotel_num!')

    if message.text.isdigit() and 1 <= int(message.text) <= 10:
        async with state.proxy() as data:
            data['hotel_num'] = int(message.text)
        await message.answer('Загружать фото отелей?', reply_markup=kb_yn)
        await FSMCustom.next()
    else:
        logger.debug(f'Пользователь {message.from_user.full_name}({message.from_user.id}) - Ошибка ввода кол-ва отелей')
        await message.reply('Не верный ввод кол-ва отелей (от 1 до 10)', reply_markup=kb_foto_num)


async def step_foto(message: types.Message, state: FSMContext) -> None:
    """
    Запись ответа пользователя в словарь
    :param message:
    :param state:
    :return:
    """
    logger.info(f'Custom Пользователь в функции load_foto!')

    if message.text.lower() in ['да', 'нет', 'yes', 'no']:
        async with state.proxy() as data:
            if message.text.lower() in ['да', 'yes']:
                data['foto'] = True
            else:
                data['foto'] = False
        logger.info(f'Пользователь ({message.from_user.id}) {data["city_dict"][data["city"]]} ({data["city"]}), '
                    f'Custom, hotel_num={data["hotel_num"]}, foto={data["foto"]}')
        await message.answer(f'Введите мини мальную и макимальную цену отеля, без запятых через пробел', reply_markup=ReplyKeyboardRemove())
        await FSMCustom.next()
    else:
        logger.debug(f'Пользователь {message.from_user.full_name}({message.from_user.id}) '
                     f'- Ошибка ввода фото')
        await message.reply('Неверный ввод (да или нет)', reply_markup=kb_yn)


async def save_price(message: types.Message, state: FSMContext) -> None:
    """
    Сохранение минимальной и максимальной цены
    :param state:
    :param message:
    :return:
    """
    price = message.text.split(" ")
    if len(price) == 2:
        async with state.proxy() as data:
            min_count = int(price[0])
            max_count = int(price[1])
            await message.answer(f'Запрос обрататывается...', reply_markup=ReplyKeyboardRemove())
            await end_fsm(message, state, min_count, max_count)
    else:
        logger.debug(f'Пользователь {message.from_user.full_name}({message.from_user.id}) '
                     f'- Ошибка ввода фото')
        await message.reply('Неверный ввод (да или нет)', reply_markup=kb_yn)


async def end_fsm(message: types.Message, state: FSMContext, min, max) -> None:
    """
    Поиск отелей
    :param message:
    :param state:
    :return:
    """
    async with state.proxy() as data:
        all_hotel = await search_hotel.s_hotel(message.from_user.id,
                                               data["city"],
                                               data["hotel_num"],
                                               data["foto"],
                                               'custom',
                                               min_cust=min,
                                               max_cust=max)
        if all_hotel:
            await bot.send_message(message.from_user.id, f'Поиск завершён', reply_markup=inline_keyboard_help())
            user_add(message)
            result = dict()
            result['hotels'] = all_hotel
            result['hotel_num'] = len(all_hotel)
            result['city'] = data["city_dict"][data["city"]]
            result['city_id'] = data["city"]
            request_add(message, 'custom', result)
        else:
            await bot.send_message(message.from_user.id, f'В выбранном городе отелей не найдено',
                                   reply_markup=inline_keyboard_help())
    await state.finish()


def register_custom_handlers(disp: Dispatcher) -> None:
    """
    Регистрация функций
    :param disp:
    :return:
    """
    disp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    disp.register_callback_query_handler(start_fsm, text='/custom')
    disp.register_message_handler(start_fsm, commands=['custom'])
    disp.register_message_handler(step_city, state=FSMCustom.step_1)
    disp.register_message_handler(step_not_city, state=FSMCustom.step_2)
    disp.register_callback_query_handler(step_load_city, state=FSMCustom.step_2)
    disp.register_message_handler(step_hotel_num, state=FSMCustom.step_3)
    disp.register_message_handler(step_foto, state=FSMCustom.step_4)
    disp.register_message_handler(save_price, state=FSMCustom.step_5)
