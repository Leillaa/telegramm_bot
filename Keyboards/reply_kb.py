from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from Config.config import DEFAULT_COMMANDS


def kb_generator(cities):
    kb_gen = ReplyKeyboardMarkup(resize_keyboard=True)
    for i_city, i_code in cities.items():
        kb_gen.insert(i_city, )
    return kb_gen


# клавиатура да/нет
kb_yn = ReplyKeyboardMarkup(resize_keyboard=True)
kb_1_1 = KeyboardButton('Да')
kb_1_2 = KeyboardButton('Нет')
kb_cancel = KeyboardButton('Отмена')
kb_yn.row(kb_1_1, kb_1_2, kb_cancel)


# клавиатура из DEFAULT_COMMANDS для help
kb_help = ReplyKeyboardMarkup(resize_keyboard=True)
for i_button in DEFAULT_COMMANDS:
    kb_help.insert('/' + i_button[0], )


# клавиатура выбора количества фото для отелей
kb_foto_num = ReplyKeyboardMarkup(resize_keyboard=True)
kb_3_1 = KeyboardButton('1')
kb_3_2 = KeyboardButton('3')
kb_3_3 = KeyboardButton('5')
kb_foto_num.row(kb_3_1, kb_3_2, kb_3_3, kb_cancel)


# клавистура отмены
kb_reply_cancel = ReplyKeyboardMarkup(resize_keyboard=True).add(kb_cancel)