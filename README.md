📌 1. Опис структури проєкту та технологій
        🧩 Загальна архітектура

        Проєкт являє собою Telegram-бота для керування інтернет-послугами провайдера (РО-НЕТ). Бот дозволяє користувачам:

        переглядати стан мережі та пристроїв
        перевіряти швидкість інтернету
        керувати тарифом
        оплачувати послуги через Monobank
        ставити інтернет на паузу
        створювати заявки в техпідтримку
        переглядати історію платежів
        редагувати профіль

        Структура проєкту
        project/
        │
        ├── main.py                  # Точка входу (запуск бота)
        ├── config.py                # Конфігурація (токени, DB URL)
        │
        ├── bot/
        │   ├── handlers/           # Обробники команд та кнопок
        │   │   ├── start.py
        │   │   ├── menu.py
        │   │   ├── dashboard.py
        │   │   ├── speedtest.py
        │   │   ├── wifi.py
        │   │   ├── support.py
        │   │   ├── tariffs.py
        │   │   ├── profile.py
        │   │   ├── pause_internet.py
        │   │   ├── restart_connection.py
        │   │   ├── mono_payment.py
        │   │   └── payments_history.py
        │   │
        │   └── keyboards/          # Клавіатури Telegram
        │       └── main.py
        │
        ├── database/
        │   ├── session.py          # Підключення до БД
        │   ├── models.py           # SQLAlchemy моделі
        │   └── repo.py             # CRUD операції
        │
        ├── services/
        │   └── mono_service.py     # Робота з Monobank API
        │
        ├── temp/                   # Тимчасові файли (QR-коди)
        │
        └── .env                    # Змінні середовища

       Використані технології
        Backend
        Python 3.10+
        asyncio (асинхронна логіка)
        logging
        Telegram Bot
        aiogram 3.x (основний фреймворк)
        FSM (Finite State Machine) для сценаріїв
        🗄 База даних
        SQLAlchemy (async ORM)
        SQLite (за замовчуванням, через aiosqlite)
        💳 Платежі
        Monobank Merchant API
        aiohttp (HTTP запити)
        📡 Додаткові сервіси
        speedtest-cli (перевірка швидкості інтернету)
        qrcode (генерація QR для Wi-Fi)

📌 2. Інструкція встановлення, налаштування та запуску
    🖥 1. Клонування проєкту
    git clone https://github.com/your-repo/ro-net-bot.git
    cd ro-net-bot
    📥 2. Встановлення залежностей
    pip install -r requirements.txt
    Якщо файлу немає, основні залежності:
    pip install aiogram sqlalchemy aiosqlite aiohttp python-dotenv speedtest-cli qrcode
    🔐 3. Налаштування .env
    Створити файл .env:
    BOT_TOKEN=your_telegram_bot_token
    MONO_TOKEN=your_monobank_token
    DATABASE_URL=sqlite+aiosqlite:///bot_database.db
    🗄 4. Ініціалізація бази даних
    База створюється автоматично при запуску:
    await init_db()
    ▶️ 5. Запуск бота
    python main.py
    Після запуску в консолі:
    🤖 Бот РО-НЕТ успішно запущений!
    🚀 6. Функціонал після запуску

    Після старту користувач отримує меню:
    🏠 Дашборд мережі
    ⚡ Speedtest
    📶 Wi-Fi оптимізація
    💳 Оплата
    🧾 Історія платежів
    📋 Тарифи
    👤 Профіль
    🛠 Техпідтримка
    📦 Пауза інтернету
