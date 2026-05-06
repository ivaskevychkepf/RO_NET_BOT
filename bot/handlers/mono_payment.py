from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import MONO_TOKEN
from services.mono_service import MonoService
from database.session import get_db
from database.repo import (
    get_or_create_user,
    create_payment,
    update_payment_status
)

router = Router()
mono = MonoService(MONO_TOKEN)

class PaymentStates(StatesGroup):
    waiting_amount = State()

@router.message(F.text == "💳 Оплата")
async def payment_menu(message: Message):

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 100 грн", callback_data="pay_100")],
        [InlineKeyboardButton(text="💰 200 грн", callback_data="pay_200")],
        [InlineKeyboardButton(text="💰 500 грн", callback_data="pay_500")],
        [InlineKeyboardButton(text="✏️ Інша сума", callback_data="pay_custom")]
    ])

    await message.answer("💳 Оберіть суму оплати:", reply_markup=kb)

@router.callback_query(F.data.startswith("pay_") & ~F.data.contains("custom"))
async def create_fixed_payment(callback: CallbackQuery):

    amount = int(callback.data.split("_")[1])

    invoice = await mono.create_invoice(
        amount_uah=amount,
        desc=f"Оплата інтернету {amount} грн"
    )

    pay_url = invoice.get("pageUrl")
    invoice_id = invoice.get("invoiceId")

    async for db in get_db():

        await create_payment(
            db=db,
            telegram_id=callback.from_user.id,
            amount=amount,
            invoice_id=invoice_id
        )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатити", url=pay_url)],
        [InlineKeyboardButton(text="🔄 Перевірити оплату", callback_data=f"check_{invoice_id}")]
    ])

    await callback.message.edit_text(
        f"💳 Рахунок створено\n\n"
        f"💰 Сума: {amount} грн",
        reply_markup=kb
    )

@router.callback_query(F.data == "pay_custom")
async def custom_amount_start(callback: CallbackQuery, state: FSMContext):

    await callback.message.answer("✏️ Введіть суму оплати (грн):")
    await state.set_state(PaymentStates.waiting_amount)

@router.message(PaymentStates.waiting_amount)
async def custom_amount_handler(message: Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer("❌ Введіть число (наприклад 150)")
        return

    amount = int(message.text)

    invoice = await mono.create_invoice(
        amount_uah=amount,
        desc=f"Оплата інтернету {amount} грн"
    )

    pay_url = invoice.get("pageUrl")
    invoice_id = invoice.get("invoiceId")

    async for db in get_db():

        await create_payment(
            db=db,
            telegram_id=message.from_user.id,
            amount=amount,
            invoice_id=invoice_id
        )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатити", url=pay_url)],
        [InlineKeyboardButton(text="🔄 Перевірити оплату", callback_data=f"check_{invoice_id}")]
    ])

    await message.answer(
        f"💳 Рахунок створено\n\n"
        f"💰 Сума: {amount} грн",
        reply_markup=kb
    )

    await state.clear()

@router.callback_query(F.data.startswith("check_"))
async def check_payment(callback: CallbackQuery):

    invoice_id = callback.data.replace("check_", "")

    status = await mono.get_invoice_status(invoice_id)

    if status.get("status") == "success":

        amount = status.get("amount", 0) / 100

        async for db in get_db():

            await update_payment_status(
                db=db,
                invoice_id=invoice_id,
                status="success"
            )

            user = await get_or_create_user(db, callback.from_user.id)

            user.balance += amount
            await db.commit()

        await callback.message.edit_text(
            f"✅ Оплата успішна!\n"
            f"💰 +{amount:.2f} грн зараховано\n"
            f"📡 Баланс оновлено"
        )

    else:
        await callback.message.answer("⏳ Оплата ще не підтверджена")