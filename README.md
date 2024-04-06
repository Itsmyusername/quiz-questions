# Бот-викторина

Телеграм и vk-бот для проведения игры Викторина.

## Установка

```commandline
git clone https://github.com/Itsmyusername/quiz-questions.git
```

## Установка зависимостей

```commandline
pip install -r requirements.txt
```

## Предварительная подготовка

### redis DB
Этот проект использует базу данных Redis. Создайте и подключите ваш экземпляр на [redis website](https://app.redislabs.com/)

### env variables

Для настройки параметров создайте файл .env в корневой папке проекта и поместите в него следующее:

#### Типичные настройки

- `TELEGRAM_BOT_TOKEN` - Токен доступа вашего бота. Вы получаете его от бота [BotFather Telegram bot](https://t.me/BotFather)
- `TELEGRAM_LOGGING_BOT_TOKEN` - то же самое, что и выше, но используется для отправки логов. Может быть тем же самым ботом или отдельным.
- `TELEGRAM_USER_ID` - Ваш числовой ID в Telegram. Можно проверить, написав 
- `LOGGING_LEVEL` - Желаемый [logging level](https://docs.python.org/3/library/logging.html#logging-levels)
- `REDIS_HOST` - Хост вашей базы данных Redis
- `REDIS_PORT` - Порт вашей базы данных Redis
- `REDIS_PASSWORD` - Пароль для вашей базы данных Redis
- `REDIS_DB_NUMBER` - ID вашей базы данных Redis
- `QUIZ_FILE_PATH` - Путь к файлу с викториной в кодировке KOI8-R (см. quiz_questions/example.txt)

## Как использовать

Боты для Telegram и VK являются отдельными и должны быть запущены путём выполнения tg_bot.py и vk_bot.py.

```commandline
python tg_bot.py  # запускает бота Telegram 
python vk_bot.py  # запускает бота VK 
```

Чтобы бот Telegram мог отправлять сообщения, отправьте ему команду /start.
