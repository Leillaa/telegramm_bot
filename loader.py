import os
import sys
from loguru import logger
from aiogram import Bot
from aiogram.types import BotCommand
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Config.config import DEFAULT_COMMANDS, BOT_TOKEN


def log_func() -> None:
    """
    Настройки loguru
    :return:
    """
    logger.remove()
    base_dir = os.getcwd()
    logger.add(f'{base_dir}/logs/debug.log',
               format='{time:YYYY-MM-DD HH:mm} | {level} | {message} | {file.path}:{function}',
               level='DEBUG',
               rotation='10 KB')
               # compression='zip')
    logger.add(f'{base_dir}/logs/error.log',
               format='{time:YYYY-MM-DD HH:mm} | {level} | {message} | {file.path}:{function}',
               level='ERROR',
               rotation='10 KB')
               # compression='zip')
    logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm}</green> | <level>{message}</level> | "
                                                 "{file}:{function}")



async def shutdown(storage) -> None:
    """
    Функция чистит память для машины состояний
    :param dp:
    :return:
    """
    # await storage.close()
    logger.info('Бот закончил свою работу!')


async def setup_bot_commands(_) -> None:
    """
    Загрузка в бот команд по умолчанию
    :param _:
    :return:
    """
    await bot.set_my_commands([BotCommand(*i) for i in DEFAULT_COMMANDS])
    logger.info('Бот запущен!')


async def setup_bot_commands(_) -> None:
    """
    Загрузка в бот команд по умолчанию
    :param _:
    :return:
    """
    await bot.set_my_commands([BotCommand(*i) for i in DEFAULT_COMMANDS])
    logger.info('Бот запущен!')

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)
