import asyncio
import logging
import os

from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Update

from config import BOT_TOKEN
from database.session import init_db

from bot.handlers import (
    start, menu, dashboard, speedtest, wifi, support,
    tariffs, profile, pause_internet, restart_connection,
    mono_payment, payments_history
)

# ===== BOT INIT =====
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

# Роутери
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

# ===== FASTAPI =====
app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()

    # встановлюємо webhook автоматично
    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        await bot.set_webhook(webhook_url)

    logging.info("🤖 Бот запущено через webhook!")


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot=bot, update=update)
    return {"ok": True}
