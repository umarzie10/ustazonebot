from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.keyboards.menu import get_socials_menu

router = Router()

@router.callback_query(F.data == "socials")
async def cq_socials(callback: CallbackQuery):
    text = "📱 <b>Bizni ijtimoiy tarmoqlarda kuzating</b>\n\nUstaZone yangiliklari, foydali maslahatlar va yangi imkoniyatlardan xabardor bo‘ling."
    await callback.message.edit_text(text, reply_markup=get_socials_menu())
