import sqlite3 as sq
import os
import time
from Config.config import HISTORY_NUM
from Config.config import DB_NAME
from loguru import logger
from aiogram.types import Message


def time_formate(t: float):
    named_tuple = time.localtime(t)  # получить struct_time
    time_string = time.strftime("%d.%m.%Y %H:%M", named_tuple)
    return time_string


def requests_tbl(func):
    """
    Декоратор, который позволяет работать с таблицей requests
    :param func:
    :return:
    """

    def wraped_func(*args, **kwargs):
        con = None
        try:
            file_name = 'database' + os.path.sep + DB_NAME
            con = sq.connect(file_name)
            cur = con.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS requests(
                    id INTEGER,
                    command TEXT,
                    time TEXT,
                    hotels TEXT)
                    ''')
            value = func(cur, *args, **kwargs)
            con.commit()
            logger.info('Таблица requests создана/открыта! ')
            return value
        except sq.Error as e:
            if con:
                con.rollback()
                logger.error('1: Ошибка создания таблицы requests! ')
        finally:
            if con:
                con.close()
                logger.info('Таблица requests закрыта! ')
    return wraped_func


def users_tbl(func):
    """
    Декоратор, который позволяет работать с таблицей users
    :param func:
    :return:
    """

    def wraped_func(*args, **kwargs):
        con = None
        try:
            file_name = 'database' + os.path.sep + DB_NAME
            con = sq.connect(file_name)
            cur = con.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS users(
                    user_id INTEGER PRIMARY KEY,
                    user_name TEXT,
                    user_rights TEXT DEFAULT 'user',
                    user_lang TEXT DEFAULT 'ru')
                    ''')
            value = func(cur, *args, **kwargs)
            con.commit()
            logger.info('Таблица users создана/открыта! ')
            return value
        except sq.Error as e:
            if con:
                con.rollback()
                print('Ошибка создания/записи таблицы users! Данные не записаны!', e)
        finally:
            if con:
                con.close()
                logger.info('Таблица users закрыта! ')
    return wraped_func


@requests_tbl
def request_add(cur, message: Message, command, rezult):
    """
    Записывает данные в таблицу requests
    :param cur:
    :param message:
    :param command:
    :param rezult:
    """
    try:
        cur.execute('INSERT INTO requests VALUES (?, ?, ?, ?)', (message.from_user.id, command,
                                                                 time_formate(time.time()), str(rezult)))
        logger.info(f'Данные записаны в таблицу requests {cur.lastrowid}')
    except Exception as e:
        logger.error('Ошибка записи в таблицу requests')


@requests_tbl
def user_history(cur, user_id):
    cur.execute('SELECT _rowid_, command, time, hotels FROM requests WHERE id LIKE ? ORDER BY _rowid_ DESC', (user_id,))
    selected_history = cur.fetchmany(HISTORY_NUM)
    result = {}
    for i_value in selected_history:
        h_req = eval(i_value[3])
        result[i_value[0]] = {
            'request': i_value[1],
            'time': i_value[2],
            'city_id': h_req['city_id'],
            'city': h_req['city'],
            'hotel_num': h_req['hotel_num'],
            'hotels': h_req['hotels']
        }
    return result


@users_tbl
def user_add(cur, message: Message) -> None:
    """
    Записывает пользователя в таблицу users
    :param cur:
    :param message:
    """
    cur.execute('SELECT count() as count FROM users WHERE user_id=?', (message.from_user.id, ))
    num = cur.fetchall()
    if num[0][0]:
        logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) уже существует в таблице users')
    else:
        cur.execute('INSERT INTO users VALUES (?, ?, "user", "ru")', (message.from_user.id, message.from_user.full_name))
        logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) записан в таблицу users')


