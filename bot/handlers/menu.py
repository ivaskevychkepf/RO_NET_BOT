from aiogram import Router, F
from aiogram.types import Message

from bot.handlers.dashboard import show_dashboard

router = Router()

@router.message(F.text == "🏠 Мережевий Дашборд")
async def open_dashboard(message: Message):
    await show_dashboard(message)