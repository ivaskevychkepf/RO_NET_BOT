import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from database.session import init_db

from bot.handlers import start, menu, dashboard, speedtest, wifi, support, tariffs, profile, pause_internet, restart_connection, mono_payment, payments_history


async def main():
    await init_db()

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Реєстрація роутерів
    dp.include_router(start.router)
    dp.include_router(menu.router)
    dp.include_router(dashboard.router)
    dp.include_router(speedtest.router)
    dp.include_router(wifi.router)
    dp.include_router(support.router)
    dp.include_router(tariffs.router)
    dp.include_router(profile.router)
    dp.include_router(pause_internet.router)
    dp.include_router(restart_connection.router)
    dp.include_router(mono_payment.router)
    dp.include_router(payments_history.router)

    logging.info("🤖 Бот РО-НЕТ успішно запущений!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())