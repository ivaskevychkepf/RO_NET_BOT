from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="🏠 Мережевий Дашборд")],
        [KeyboardButton(text="⚡ Перевірити швидкість")],
        [KeyboardButton(text="📶 Оптимізувати Wi-Fi")],
        [KeyboardButton(text="👤 Мій профіль")],

        [KeyboardButton(text="💳 Оплата"), KeyboardButton(text="🛠 Техпідтримка")],
        [KeyboardButton(text="📋 Тарифи")],

        [KeyboardButton(text="📦 Пауза інтернету")],
        [KeyboardButton(text="🧾 Історія платежів"), KeyboardButton(text="⚙️ Перезапуск з'єднання")],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)