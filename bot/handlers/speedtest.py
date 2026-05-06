import asyncio
import speedtest
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

router = Router()


async def run_speedtest(message: Message, edit: bool = False):
    if not edit:
        status_msg = await message.answer("⚡ <b>Запускаємо тест швидкості...</b>\n\n"
                                          "🔍 Пошук найкращого сервера...")

    try:
        loop = asyncio.get_running_loop()
        
        await status_msg.edit_text("⚡ Пошук найкращого сервера...")

        def test_speed():
            st = speedtest.Speedtest()
            st.get_best_server()
            download = st.download() / 1_000_000  
            upload = st.upload() / 1_000_000      
            ping = st.results.ping
            return download, upload, ping

        download, upload, ping = await loop.run_in_executor(None, test_speed)

        text = f"""<b>⚡ Результати тесту швидкості</b>

📡 Пінг: <b>{ping:.1f} мс</b> {'🟢' if ping < 20 else '🟡' if ping < 40 else '🔴'}

⬇️ Завантаження: <b>{download:.1f} Мбіт/с</b>
⬆️ Відвантаження: <b>{upload:.1f} Мбіт/с</b>

────────────────────
✅ Тест виконано через speedtest.net
"""

    except Exception as e:
        text = f"❌ Помилка під час тесту:\n{str(e)}\n\nСпробуйте ще раз пізніше."

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Повторити тест", callback_data="retest_speed")]
    ])

    if edit:
        await message.edit_text(text, reply_markup=kb)
    else:
        await status_msg.edit_text(text, reply_markup=kb)


@router.message(F.text == "⚡ Перевірити швидкість")
async def speedtest_handler(message: Message):
    await run_speedtest(message, edit=False)


@router.callback_query(F.data == "retest_speed")
async def retest_speed(callback: CallbackQuery):
    await callback.answer("🔄 Запускаємо новий тест...")
    await run_speedtest(callback.message, edit=True)