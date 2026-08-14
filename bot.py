import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram import F

# Bot tokenini shu yerga kiriting
# BotFathern-dan olingan tokenni yozing
BOT_TOKEN = "8783456741:AAHMV3kq4oj9PidW9xmVR6hD50sizXlVu4s"

# Bot va Dispatcher yaratish
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Bosh menyu klaviaturasini yaratish funksiyasi
def get_main_menu():
    # Saytni ochish uchun WebApp yoki URL ishlatish mumkin. Hozir URL orqali ko'rsatilgan.
    keyboard = [
        [InlineKeyboardButton(text="🌐 Saytni ochish", url="https://usta-zone-uz.vercel.app/", style="primary")], 
        [InlineKeyboardButton(text="✉️ Xabar yozish", callback_data="write_message", style="success")],
        [InlineKeyboardButton(text="📢 Yangiliklar", url="https://t.me/ustazone_uz", style="primary")],
        [
            InlineKeyboardButton(text="❓ Yordam", callback_data="faq_menu", style="primary"),
            InlineKeyboardButton(text="ℹ️ Haqida", callback_data="about", style="primary")
        ],
        [InlineKeyboardButton(text="📱 Ijtimoiy tarmoqlar", callback_data="socials", style="primary")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# /start komandasi uchun xendler
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    text = "🏠 Bosh menyu\n\nKerakli bo'limni tanlang:"
    await message.answer(text, reply_markup=get_main_menu())

# Tugmalar bosilganda ishlaydigan xendler
@dp.callback_query()
async def callbacks_handler(callback: types.CallbackQuery):
    if callback.data == "write_message":
        await callback.message.answer("Siz xabar yozish bo'limini tanladingiz. Xabaringizni yozib qoldiring:")
    elif callback.data == "news":
        await callback.message.answer("Bu yerda eng so'nggi yangiliklar chiqadi.")
    elif callback.data == "faq":
        await callback.message.answer("Bu yerda ko'p beriladigan savollarga javoblar bo'ladi.")
    elif callback.data == "about":
        await callback.message.answer("Bizning loyihamiz haqida ma'lumot...")
    elif callback.data == "socials":
        await callback.message.answer("Bizning ijtimoiy tarmoqlarimiz:\n\nTelegram: https://t.me/ustazone_uz")
        
    # Telegram tomonidan "loading" animatsiyasini to'xtatish uchun
    await callback.answer()

async def main():
    # Loglarni sozlash (xatoliklarni ko'rish uchun)
    logging.basicConfig(level=logging.INFO)
    
    print("Bot ishga tushdi...")
    # Botni ishga tushirish
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
