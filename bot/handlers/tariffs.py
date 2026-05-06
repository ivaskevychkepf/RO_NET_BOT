from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from database.session import get_db
from database.repo import get_or_create_user, change_user_tariff

router = Router()

tariffs = {
    "Стартовий": {
        "speed": "100 Мбіт/с",
        "price": 299,
        "description": "Підходить для перегляду відео, соцмереж та роботи з 1-2 пристроїв."
    },
    "Оптимальний": {
        "speed": "300 Мбіт/с",
        "price": 399,
        "description": "Найпопулярніший! Ідеально для сім'ї, онлайн-ігор, кількох пристроїв одночасно."
    },
    "Максимальний": {
        "speed": "500 Мбіт/с",
        "price": 499,
        "description": "Для активних користувачів: 4K стрімінг, великий будинок, багато техніки."
    },
    "Гігабіт": {
        "speed": "1000 Мбіт/с",
        "price": 699,
        "description": "Максимальна швидкість. Для професіоналів, стрімерів та великих офісів."
    }
}


@router.message(F.text == "📋 Тарифи")
async def show_tariffs(message: Message):
    async for db in get_db():
        user = await get_or_create_user(db, message.from_user.id)

        text = f"""<b>📋 Тарифи РО-НЕТ</b>

Ваш поточний тариф: <b>{user.tariff}</b>
Баланс: <b>{user.balance:.2f} грн</b>

Оберіть тариф нижче 👇"""

        kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Стартовий — 299 грн")],
                [KeyboardButton(text="Оптимальний — 399 грн 🔥")],
                [KeyboardButton(text="Максимальний — 499 грн")],
                [KeyboardButton(text="Гігабіт — 699 грн")],
                [KeyboardButton(text="🔙 Головне меню")]
            ],
            resize_keyboard=True
        )

        await message.answer(text, reply_markup=kb)
        break


@router.message(F.text.startswith("Стартовий"))
async def show_starter_info(message: Message):
    await show_tariff_details(message, "Стартовий")


@router.message(F.text.startswith("Оптимальний"))
async def show_optimal_info(message: Message):
    await show_tariff_details(message, "Оптимальний")


@router.message(F.text.startswith("Максимальний"))
async def show_max_info(message: Message):
    await show_tariff_details(message, "Максимальний")


@router.message(F.text.startswith("Гігабіт"))
async def show_gigabit_info(message: Message):
    await show_tariff_details(message, "Гігабіт")


async def show_tariff_details(message: Message, tariff_name: str):
    tariff = tariffs[tariff_name]
    price = tariff["price"]

    text = f"""<b>{tariff_name} тариф</b>

➤ Швидкість: <b>{tariff['speed']}</b>
➤ Ціна: <b>{price} грн / місяць</b>

📝 Опис:
{tariff['description']}

────────────────────
Баланс: <b>{(await get_user_balance(message.from_user.id)):.2f} грн</b>"""

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f"✅ Підтвердити зміну на {tariff_name}")],
            [KeyboardButton(text="🔙 Скасувати")]
        ],
        resize_keyboard=True
    )

    await message.answer(text, reply_markup=kb)


async def get_user_balance(telegram_id: int):
    async for db in get_db():
        user = await get_or_create_user(db, telegram_id)
        return user.balance


@router.message(F.text.startswith("✅ Підтвердити зміну"))
async def confirm_change(message: Message):
    tariff_name = message.text.replace("✅ Підтвердити зміну на ", "").strip()
    price = tariffs[tariff_name]["price"]

    async for db in get_db():
        user = await get_or_create_user(db, message.from_user.id)

        if user.balance < price:
            await message.answer("❌ Недостатньо коштів на балансі!")
            return

        await change_user_tariff(db, message.from_user.id, tariff_name, price)

        await message.answer(
            f"✅ <b>Тариф успішно змінено!</b>\n\n"
            f"Новий тариф: <b>{tariff_name}</b>\n"
            f"Списано: <b>-{price} грн</b>",
            reply_markup=None
        )

        from bot.keyboards.main import get_main_menu
        await message.answer("🏠 Головне меню:", reply_markup=get_main_menu())
        break


@router.message(F.text == "🔙 Скасувати")
async def cancel_change(message: Message):
    from bot.keyboards.main import get_main_menu
    await message.answer("❌ Зміна тарифу скасована.", reply_markup=get_main_menu())