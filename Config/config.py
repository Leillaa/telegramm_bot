import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

# Глобльные переменные
BOT_TOKEN: str = os.getenv('BOT_TOKEN')
RAPID_API_KEY: str = os.getenv('RAPID_API_KEY')

# Команды
DEFAULT_COMMANDS: tuple = (
    ('start', "Запустить бота"),
    ('help', "Команды бота"),
    ('lowprice', 'Топ самых дешевых отелей'),
    ('highprice', 'Топ самых дорогих отелей'),
    ('custom', 'Отели по диапозону цены'),
    ('history', 'История запросов')
)

# Бза данных
DB_NAME: str = 'bot_base.db'

# Максимальное количество запросов в history
HISTORY_NUM: int = 5
