from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from bot.keyboards.main import get_main_menu
from database.repo import get_or_create_user
from database.session import get_db   # <-- додаємо

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    async for db in get_db(): 
        user = await get_or_create_user(
            db=db,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name
        )

        await message.answer(
            f"👋 Вітаємо, <b>{message.from_user.full_name}</b>!\n\n"
            "Я — розумний помічник <b>РО-НЕТ</b>.\n"
            "Тут ти можеш швидко контролювати свій інтернет.",
            reply_markup=get_main_menu()
        )
        break