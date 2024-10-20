from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Config.config import DEFAULT_COMMANDS


# Клавиатура - одна кнопка - ссылка на отель
def inline_keyboard_link(link: str) -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Ссылка на отель', url=link))
    return inline_kb


# Клавиатура - одна кнопка help
def inline_keyboard_help() -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Команды бота', callback_data='/help'))
    return inline_kb


# Клавиатура команд по умолчанию
def inline_keyboard_default() -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup()
    for item in DEFAULT_COMMANDS:
        inline_kb.add(InlineKeyboardButton(text=item[1], callback_data="/" + item[0]))
    return inline_kb


# Клавиатура городов
def kb_cities(cities) -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup()
    for i_code, i_city in cities.items():
        i_button = InlineKeyboardButton(i_city, callback_data=i_code)
        inline_kb.add(i_button)
    inline_kb.add(InlineKeyboardButton(text='== ОТМЕНА ==', callback_data='cancel'))
    return inline_kb
