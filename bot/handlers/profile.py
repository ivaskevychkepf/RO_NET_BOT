from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.session import get_db
from database.repo import get_or_create_user

router = Router()

class ProfileStates(StatesGroup):
    waiting_for_phone = State()
    waiting_for_address = State()


@router.message(F.text == "👤 Мій профіль")
async def show_profile(message: Message):
    async for db in get_db():
        user = await get_or_create_user(db, message.from_user.id)

        text = f"""<b>👤 Мій профіль</b>

🆔 ID: <b>{user.telegram_id}</b>
👤 Ім'я: <b>{user.full_name}</b>
📱 Телефон: <b>{user.phone or 'Не вказано'}</b>
📍 Адреса: <b>{user.address or 'Не вказано'}</b>

💰 Баланс: <b>{user.balance:.2f} грн</b>
📦 Тариф: <b>{user.tariff}</b>
🟢 Статус: <b>{"Активний" if user.is_active else "Неактивний"}</b>

🛑 Пауза: <b>{"Так" if user.internet_paused else "Ні"}</b>
📅 До: <b>{user.pause_until or '—'}</b>
"""

        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📱 Змінити телефон")],
                [KeyboardButton(text="📍 Змінити адресу")],
                [KeyboardButton(text="🔙 Головне меню")]
            ],
            resize_keyboard=True
        )

        await message.answer(text, reply_markup=kb)
        break

@router.message(F.text == "📱 Змінити телефон")
async def change_phone_start(message: Message, state: FSMContext):
    await message.answer("📱 Введіть новий номер телефону (наприклад: +380501234567):")
    await state.set_state(ProfileStates.waiting_for_phone)


@router.message(ProfileStates.waiting_for_phone)
async def save_phone(message: Message, state: FSMContext):
    async for db in get_db():
        user = await get_or_create_user(db, message.from_user.id)
        user.phone = message.text
        await db.commit()

    await message.answer("✅ Номер телефону успішно оновлено!", reply_markup=None)
    await show_profile(message)
    await state.clear()

@router.message(F.text == "📍 Змінити адресу")
async def change_address_start(message: Message, state: FSMContext):
    await message.answer("📍 Введіть вашу адресу підключення:")
    await state.set_state(ProfileStates.waiting_for_address)


@router.message(ProfileStates.waiting_for_address)
async def save_address(message: Message, state: FSMContext):
    async for db in get_db():
        user = await get_or_create_user(db, message.from_user.id)
        user.address = message.text
        await db.commit()

    await message.answer("✅ Адреса успішно оновлена!", reply_markup=None)
    await show_profile(message)
    await state.clear()


@router.message(F.text == "🔙 Головне меню")
async def back_to_menu(message: Message):
    from bot.keyboards.main import get_main_menu
    await message.answer("🔙 Головне меню:", reply_markup=get_main_menu())