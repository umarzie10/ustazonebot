from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.keyboards.menu import get_about_menu

router = Router()

@router.callback_query(F.data == "about")
async def cq_about(callback: CallbackQuery):
    text = (
        "💈 <b>BarberTop</b>\n\n"
        "BarberTop —\n"
        "O'zbekistondagi zamonaviy\n"
        "barbershop bron qilish platformasi.\n\n"
        "Sayt orqali:\n"
        "• Barber topish\n"
        "• Online bron qilish\n"
        "• Qulay to'lov\n"
        "• Reyting\n"
        "• Sharhlar\n\n"
        "<i>Version: 1.0.0</i>"
    )
    await callback.message.edit_text(text, reply_markup=get_about_menu())
