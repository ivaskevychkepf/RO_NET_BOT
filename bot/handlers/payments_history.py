from aiogram import Router, F
from aiogram.types import Message

from database.session import get_db
from database.repo import get_user_payments

router = Router()


@router.message(F.text == "🧾 Історія платежів")
async def payments_history(message: Message):

    async for db in get_db():
        payments = await get_user_payments(db, message.from_user.id)
        break

    if not payments:
        await message.answer("📭 У вас ще немає платежів")
        return

    text = "🧾 <b>Історія платежів</b>\n\n"

    for p in payments[:10]:
        status_emoji = "✅" if p.status == "success" else "⏳"
        text += (
            f"{status_emoji} {p.amount} грн\n"
            f"📅 {p.created_at.strftime('%Y-%m-%d %H:%M')}\n"
            f"📌 {p.status}\n\n"
        )

    await message.answer(text)