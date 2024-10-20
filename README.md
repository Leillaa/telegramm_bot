# Описание
Телеграм-бот для работы с API стороннего сайта.

# Как запустить бота
1. Клонируйте репозиторий с GitHub, создайте виртуальное окружение
и активируйте его:

$ git clone https://gitlab.skillbox.ru/leila_tagaeva/python_basic_diploma
$ python -m venv env
$ source env/bin/activate

2. Установите зависимости:

$ pip install -r requirements.txt
или
$ python -m pip install -r requirements.txt

3. Переименуйте файл .env.template в .env и укажите в нем Ваш токен для бота
и ключ от API по образцу:

BOT_TOKEN = "Ваш токен для бота, полученный от @BotFather"
RAPID_API_KEY = "Ваш ключ полученный от API по адресу rapidapi.com/apidojo/api/hotels4/"


# API

1. GET запросы:

    Запрос: v2/get-meta-data - Получение метаданных всех локаций
    Ответ:
      [
        {
          "name": "ARGENTINA",
          "posName": "HCOM_LATAM",
          "hcomLocale": "es_AR"
        },
        {
          "name": "BELIZE",
          "posName": "HCOM_LATAM",
          "hcomLocale": "es_BZ"
        },
        {
          "name": "BOLIVIA",
          "posName": "HCOM_LATAM",
          "hcomLocale": "es_BO"
        },
        {
          "name": "BRAZIL",
          "posName": "HCOM_BR",
          "hcomLocale": "pt_BR"
        },
      ]

    Запрос: locations/v3/search - Поиск по местоположению или предложению

    Запрос: reviews/v2/list - Получение отзыов о объекте недвижимости

2. POST запросы:
    
    Запрос: properties/v2/list - Список свойств с параметрами и фильтрами

    Запрос: properties/v2/get-content - Получение описания объекта недвижимости

    Запрос: properties/v2/detail - Получение подробной информации о недвижимости

    Запрос: properties/v2/get-summary - Получение сводной информации о недвижимости
    
    Запрос: reviews/v3/list - Получени е отзывов о объекте невижимости

    Запрос: reviews/v3/get-summary - Получение итоговой оценки о объекте недвижимости

    
    

# Команды бота

/start - запускает бота и выводи приветствие

/help - навигаия по боту, вывод всех доступных команд

/

/

/history - вывод истори запросов пользователя (последние 5)