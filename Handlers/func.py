from typing import Union
from loader import bot
from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from Keyboards.inline_kb import inline_keyboard_link, inline_keyboard_default
from loguru import logger


async def delete_message(call: Union[Message, CallbackQuery]):
    if type(call) == CallbackQuery:
        await call.answer(cache_time=60)
        await call.message.delete()
    else:
        await call.delete()


async def show_hotel_info(chat_id, i_value: dict) -> None:
    """
    Пишет в чат информацию об отеле
    :param chat_id:
    :param i_value:
    :return:
    """
    print(i_value)
    text = f'Отель: {i_value["name"]}\nАдрес: {i_value["address"]}\nЦена: {i_value["f_price"]}'
    if len(i_value['hotel_foto']) != 0:
        await bot.send_photo(chat_id=chat_id, photo=i_value['hotel_foto'][0], caption=text,
                             reply_markup=inline_keyboard_link(i_value['link']))
    else:
        await bot.send_message(chat_id, text, reply_markup=inline_keyboard_link(i_value['link']))


async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Выход из состояний (FSM)
    :param message:
    :param state:
    :return:
    """
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) отменил ввод!')
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Ввод отменен!', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Команды бота:', reply_markup=inline_keyboard_default())

