from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.session import get_db
from database.repo import create_ticket

router = Router()

class SupportStates(StatesGroup):
    waiting_for_description = State()


@router.message(F.text == "🛠 Техпідтримка")
async def support_menu(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Немає інтернету", callback_data="ticket_no_internet")],
        [InlineKeyboardButton(text="🐢 Повільна швидкість", callback_data="ticket_slow_speed")],
        [InlineKeyboardButton(text="📡 Проблеми з Wi-Fi", callback_data="ticket_wifi")],
        [InlineKeyboardButton(text="🔌 Проблеми з роутером", callback_data="ticket_router")],
        [InlineKeyboardButton(text="❓ Інша проблема", callback_data="ticket_other")]
    ])

    await message.answer("<b>🛠 Технічна підтримка</b>\n\nОберіть тип проблеми:", reply_markup=kb)


@router.callback_query(F.data.startswith("ticket_"))
async def ticket_type_selected(callback: CallbackQuery, state: FSMContext):
    ticket_type_map = {
        "ticket_no_internet": "Немає інтернету",
        "ticket_slow_speed": "Повільна швидкість",
        "ticket_wifi": "Проблеми з Wi-Fi",
        "ticket_router": "Проблеми з роутером",
        "ticket_other": "Інша проблема"
    }

    ticket_type = ticket_type_map.get(callback.data, "Інша")

    await state.update_data(ticket_type=ticket_type)
    await callback.message.edit_text(
        f"<b>Обрано:</b> {ticket_type}\n\n"
        "Опишіть проблему детальніше (що саме відбувається, коли почалось тощо):"
    )
    await state.set_state(SupportStates.waiting_for_description)


@router.message(SupportStates.waiting_for_description)
async def save_ticket(message: Message, state: FSMContext):
    data = await state.get_data()
    ticket_type = data.get("ticket_type", "Інша")

    async for db in get_db():
        ticket = await create_ticket(
            db=db,
            telegram_id=message.from_user.id,
            ticket_type=ticket_type,
            description=message.text
        )

    await message.answer(
        f"✅ <b>Заявка №{ticket.id} успішно створена!</b>\n\n"
        f"Тип: {ticket_type}\n"
        f"Статус: Нова\n\n"
        "Оператор зв'яжеться з вами найближчим часом."
    )
    await state.clear()