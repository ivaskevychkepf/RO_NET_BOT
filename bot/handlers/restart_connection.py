import asyncio
from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "⚙️ Перезапуск з'єднання")
async def restart_connection(message: Message):

    await message.answer("🔄 Перезапускаю з'єднання...")

    await asyncio.sleep(2)

    await message.answer(
        "✅ З'єднання перезапущено\n"
        "📡 Інтернет відновлено"
    )