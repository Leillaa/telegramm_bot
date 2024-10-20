from loguru import logger
from typing import Union
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from loader import bot
from Keyboards.inline_kb import inline_keyboard_help, inline_keyboard_default
from Handlers.func import delete_message


async def bot_start(message: Union[Message, CallbackQuery]) -> None:
    """
    Ответ на команду /start
    :param message:
    :return:
    """
    await delete_message(message)
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) выполнил команду "start"')
    await bot.send_message(message.from_user.id,
                           f"Привет, <b>{message.from_user.full_name}</b>!\n"
                           f"Этот бот умеет искать отели по запросу",
                           parse_mode='html',
                           reply_markup=inline_keyboard_help())


async def bot_help(message: Union[Message, CallbackQuery]) -> None:
    """
    Ответ на команду /help
    :param message:
    :return:
    """
    await delete_message(message)
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) выполнил команду "help"')
    await bot.send_message(message.from_user.id, f"Команды бота:\n", parse_mode='html',
                           reply_markup=inline_keyboard_default())


def register_default_handlers(disp: Dispatcher) -> None:
    disp.register_message_handler(bot_start, commands=['start'])
    disp.register_callback_query_handler(bot_start, text='/start')
    disp.register_message_handler(bot_help, commands=['help'])
    disp.register_callback_query_handler(bot_help, text='/help')
