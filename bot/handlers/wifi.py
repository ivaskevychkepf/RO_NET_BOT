import random
import asyncio
import qrcode
import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

router = Router()

os.makedirs("temp", exist_ok=True)


async def show_wifi_optimizer(message: Message, edit: bool = False):
    if not edit:
        status = await message.answer("📡 Сканую мережі навколо...")

    await asyncio.sleep(1.5)

    current_channel = random.randint(1, 11)
    best_channel = random.choice([1, 6, 11])
    signal = random.randint(70, 98)

    wifi_name = f"РО-НЕТ_{random.randint(100, 999)}"
    wifi_password = ''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789', k=12))

    text = f"""<b>📶 Оптимізація Wi-Fi</b>

🏠 Мережа: <b>{wifi_name}</b>
📡 Поточний канал: <b>{current_channel}</b>
📶 Сила сигналу: <b>{signal}%</b>

✅ <b>Рекомендації:</b>
• Оптимальний канал: <b>{best_channel}</b>
• Краще використовувати діапазон 5 ГГц
• Пароль повинен бути складним

🔑 <b>Ваш пароль:</b>
<code>{wifi_password}</code>
"""

    qr = qrcode.make(f"WIFI:S:{wifi_name};T:WPA;P:{wifi_password};;")
    qr_path = f"temp/wifi_qr_{message.from_user.id}.png"
    qr.save(qr_path)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Пересканувати", callback_data="rescan_wifi")],
        [InlineKeyboardButton(text="📱 Отримати QR-код", callback_data="send_qr")]
    ])

    if edit:
        await message.edit_text(text, reply_markup=kb)
    else:
        await status.edit_text(text, reply_markup=kb)

    await message.answer_photo(
        photo=FSInputFile(qr_path),
        caption="🔑 Відскануй цей QR-код для швидкого підключення до Wi-Fi"
    )


@router.message(F.text == "📶 Оптимізувати Wi-Fi")
async def wifi_handler(message: Message):
    await show_wifi_optimizer(message, edit=False)


@router.callback_query(F.data == "rescan_wifi")
async def rescan_wifi(callback: CallbackQuery):
    await callback.answer("🔄 Сканую...")
    await show_wifi_optimizer(callback.message, edit=True)


@router.callback_query(F.data == "send_qr")
async def send_qr(callback: CallbackQuery):
    await callback.answer("📱 Генеруємо QR-код...")
    await callback.message.answer("📱 QR-код вже надіслано вище 👆")