from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.keyboards.menu import get_yordam_menu, get_yordam_back_menu

router = Router()

@router.callback_query(F.data == "faq_menu")
async def cq_faq_menu(callback: CallbackQuery):
    text = "❓ Yordam\nQuyidagilardan birini tanlang:"
    await callback.message.edit_text(text, reply_markup=get_yordam_menu())

@router.callback_query(F.data == "faq_find")
async def cq_faq_find(callback: CallbackQuery):
    text = "🔎 Usta topish\nSiz kerakli xizmat turini tanlaysiz, joylashuvingizni ko‘rsatasiz va mavjud ustalar orasidan o‘zingizga mosini tanlaysiz."
    await callback.message.edit_text(text, reply_markup=get_yordam_back_menu())

@router.callback_query(F.data == "faq_order")
async def cq_faq_order(callback: CallbackQuery):
    text = "📋 Buyurtma qanday beriladi?\n1. Saytdan kerakli ustani tanlaysiz.\n2. Xizmat turi va vaqtni belgilaysiz.\n3. Usta tasdiqlaganidan so'ng buyurtma qabul qilinadi."
    await callback.message.edit_text(text, reply_markup=get_yordam_back_menu())

@router.callback_query(F.data == "faq_payment")
async def cq_faq_payment(callback: CallbackQuery):
    text = "💳 To‘lov qanday ishlaydi?\nTo'lov to'g'ridan-to'g'ri usta bilan naqd pul yoki karta orqali (Click/Payme) amalga oshiriladi. Sayt komissiya olmaydi."
    await callback.message.edit_text(text, reply_markup=get_yordam_back_menu())

@router.callback_query(F.data == "faq_rating")
async def cq_faq_rating(callback: CallbackQuery):
    text = "⭐ Reyting qanday beriladi?\nXizmat yakunlangach, mijoz sayt orqali ustaga baho (1 dan 5 gacha) va izoh qoldirishi mumkin. Bu keyingi mijozlarga tanlashda yordam beradi."
    await callback.message.edit_text(text, reply_markup=get_yordam_back_menu())

