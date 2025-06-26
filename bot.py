import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command

from sqlite_db import SqliteUserDataManager

# Создаем экземпляр базы данных
data = SqliteUserDataManager()

# Тут импортируем все команды, нам понадобится только старт

from commands import (
    start_command,
    allusers_command
)

# Также добавим логирование что бы видеть ошибки
# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Импорт конфигурации
from config import TOKEN

# Создаем основной роутер
main_router = Router()


# Регистрируем роутер для вызова команды /start
@main_router.message(Command("start"))
async def handle_start(message: types.Message):
    await start_command(message, data)

@main_router.message(Command("users"))
async def handle_users(message: types.Message):
    await allusers_command(message, data)


async def main():
    # Инициализация бота
    global bot
    bot = Bot(TOKEN)
    dp = Dispatcher()

    # Регистрируем роутер
    dp.include_router(main_router)

    # Запуск бота
    logger.info("🤖 Бот запущен")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
