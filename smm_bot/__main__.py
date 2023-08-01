import logging
from aiogram import Bot, Dispatcher, executor, filters

from config import TELEGRAM_BOT_TOKEN
from handlers import start, help_, other, video2

bot = Bot(TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Список пар "команда - обработчик"
command_handlers = [
    ('start', start),
    ('help', help_),
    # ('command2', command2),
    # ('command3', command3),
    # # Добавьте сюда другие команды и обработчики
]

# Регистрация команд и обработчиков из списка
for command, handler in command_handlers:
    dp.register_message_handler(handler, commands=[command])

dp.register_message_handler(other, ~filters.CommandStart())

callback_handlers = [
    ('goto_video2', video2),
    # ('goto_video3', video3),
]

for callback, handler in callback_handlers:
    dp.register_callback_query_handler(handler, lambda query, cb=callback: query.data == cb)


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)
