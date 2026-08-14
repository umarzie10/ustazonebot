from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.keyboards.menu import get_about_menu

router = Router()

@router.callback_query(F.data == "about")
async def cq_about(callback: CallbackQuery):
    text = (
        "ℹ️ <b>UstaZone haqida</b>\n\n"
        "UstaZone — mijozlarni ishonchli va malakali ustalar bilan bog‘laydigan xizmat platformasi.\n"
        "Bu yerda siz:\n"
        "• 🔎 kerakli ustani topishingiz\n"
        "• 📋 buyurtma berishingiz\n"
        "• ⭐ usta haqida fikr va reytinglarni ko‘rishingiz\n"
        "• 💬 usta bilan bog‘lanishingiz mumkin.\n\n"
        "🚀 UstaZone — kerakli usta, kerakli vaqtda."
    )
    await callback.message.edit_text(text, reply_markup=get_about_menu())
