from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.crud.faq import get_all_faqs, get_faq_by_id
from bot.keyboards.menu import get_faq_menu, get_faq_back_menu

router = Router()

@router.callback_query(F.data == "faq_menu")
async def cq_faq_menu(callback: CallbackQuery, session: AsyncSession):
    faqs = await get_all_faqs(session)
    if not faqs:
        await callback.answer("Hozircha FAQ mavjud emas.", show_alert=True)
        return
        
    text = "❓ <b>Ko'p beriladigan savollar (FAQ)</b>\n\nQiziqtirgan savolingizni tanlang:"
    await callback.message.edit_text(text, reply_markup=get_faq_menu(faqs))

@router.callback_query(F.data.startswith("faq_item_"))
async def cq_faq_item(callback: CallbackQuery, session: AsyncSession):
    faq_id = int(callback.data.split("_")[2])
    faq = await get_faq_by_id(session, faq_id)
    
    if not faq:
        await callback.answer("Savol topilmadi.", show_alert=True)
        return
        
    text = f"❓ <b>{faq.question}</b>\n\n{faq.answer}"
    await callback.message.edit_text(text, reply_markup=get_faq_back_menu())
