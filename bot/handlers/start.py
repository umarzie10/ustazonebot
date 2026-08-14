from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from bot.keyboards.menu import get_main_menu

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    text = "🏠 Bosh menyu\n\nKerakli bo'limni tanlang:"
    await message.answer(text, reply_markup=get_main_menu())

@router.callback_query(F.data == "main_menu")
async def cq_main_menu(callback: CallbackQuery):
    text = "🏠 Bosh menyu\n\nKerakli bo'limni tanlang:"
    await callback.message.edit_text(text, reply_markup=get_main_menu())
