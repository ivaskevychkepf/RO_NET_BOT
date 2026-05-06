from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from database.session import get_db
from database.repo import pause_internet, cancel_pause, get_user

router = Router()

@router.message(F.text == "📦 Пауза інтернету")
async def pause_menu(message: Message):

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏸ 3 дні", callback_data="pause_3")],
        [InlineKeyboardButton(text="⏸ 7 днів", callback_data="pause_7")],
        [InlineKeyboardButton(text="⏸ 14 днів", callback_data="pause_14")],
        [InlineKeyboardButton(text="🔓 Скасувати паузу", callback_data="pause_cancel")]
    ])

    async for db in get_db():
        user = await get_user(db, message.from_user.id)

        if not user:
            await message.answer("❌ Користувача не знайдено в базі")
            return

        status = "⏸ АКТИВНА" if user.internet_paused else "🟢 НІ"

        await message.answer(
            f"📦 Пауза інтернету\n\n"
            f"Статус: {status}\n\n"
            f"Оберіть дію:",
            reply_markup=kb
        )
        break

@router.callback_query(F.data.startswith("pause_"))
async def set_pause(callback: CallbackQuery):

    if callback.data == "pause_cancel":
        async for db in get_db():
            await cancel_pause(db, callback.from_user.id)
        await callback.message.edit_text("🔓 Пауза скасована\n🟢 Інтернет активний")
        return

    days = int(callback.data.split("_")[1])

    async for db in get_db():
        end_date = await pause_internet(db, callback.from_user.id, days)

    await callback.message.edit_text(
        f"📦 Інтернет призупинено\n\n"
        f"⏸ {days} днів\n"
        f"📅 До: {end_date.strftime('%Y-%m-%d')}\n\n"
        f"🔓 Відновиться автоматично"
    )