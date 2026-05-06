import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.main import get_main_menu
from database.repo import get_or_create_user
from database.session import get_db

router = Router()


async def generate_dashboard_text(user):
    devices_online = random.randint(2, 7)
    total_devices = 8
    speed = random.randint(45, 95)
    ping = random.randint(8, 25)
    
    active_devices = ["Телевізор Samsung", "Ноутбук Lenovo", "iPhone 15", 
                     "ПК Gaming", "Планшет Xiaomi", "Камера"]
    most_active = random.choice(active_devices)

    full_name = user.full_name or "Користувач"

    text = f"""<b>🏠 Мережевий Дашборд</b>

👤 Абонент: <b>{full_name}</b>
📍 Адреса: <b>{user.address or 'Не вказано'}</b>

🔋 Баланс: <b>{user.balance:.2f} грн</b>
📦 Тариф: <b>{user.tariff}</b>
🟢 Статус: <b>Онлайн</b>

────────────────────
📡 Пристроїв онлайн: <b>{devices_online}</b> з {total_devices}
📶 Середня швидкість: <b>{speed} Мбіт/с</b>
⏱ Пінг: <b>{ping} мс</b>

🔥 Найактивніший зараз: <b>{most_active}</b>
"""
    return text


async def show_dashboard(message_or_callback, edit: bool = False):
    if isinstance(message_or_callback, CallbackQuery):
        telegram_id = message_or_callback.from_user.id
        message = message_or_callback.message
    else:
        telegram_id = message_or_callback.from_user.id
        message = message_or_callback

    async for db in get_db():
        user = await get_or_create_user(
            db=db,
            telegram_id=telegram_id,
            username=message_or_callback.from_user.username if hasattr(message_or_callback, 'from_user') else None,
            full_name=message_or_callback.from_user.full_name if hasattr(message_or_callback, 'from_user') else None
        )

        text = await generate_dashboard_text(user)

        refresh_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Оновити дані", callback_data="refresh_dashboard")]
        ])

        if edit:
            await message.edit_text(text, reply_markup=refresh_kb)
        else:
            await message.answer(text, reply_markup=refresh_kb)
        break


@router.message(F.text == "🏠 Мережевий Дашборд")
async def dashboard_handler(message: Message):
    await show_dashboard(message, edit=False)


@router.callback_query(F.data == "refresh_dashboard")
async def refresh_dashboard(callback: CallbackQuery):
    await callback.answer("🔄 Оновлюємо...")
    await show_dashboard(callback, edit=True)