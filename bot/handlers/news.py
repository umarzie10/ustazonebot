from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.crud.news import get_news_count, get_news_paginated
from bot.keyboards.menu import get_news_pagination, get_main_menu

router = Router()

@router.callback_query(F.data.startswith("news_page_"))
async def cq_news_page(callback: CallbackQuery, session: AsyncSession):
    page = int(callback.data.split("_")[2])
    
    total_news = await get_news_count(session)
    if total_news == 0:
        await callback.message.edit_text(
            "📢 Hozircha yangiliklar mavjud emas.",
            reply_markup=get_main_menu()
        )
        return
        
    news_items = await get_news_paginated(session, offset=page, limit=1)
    if not news_items:
        await callback.answer("Yangilik topilmadi.", show_alert=True)
        return
        
    news = news_items[0]
    date_str = news.created_at.strftime("%d.%m.%Y %H:%M")
    
    text = f"📢 <b>{news.title}</b>\n\n{news.text}\n\n<i>📅 Sana: {date_str}</i>"
    
    reply_markup = get_news_pagination(page=page, total=total_news)
    
    # If the message has a photo but the new news doesn't, or vice-versa, we have to handle it.
    # To keep things simple and avoid edit_media errors when media type changes, 
    # it's better to delete the message and send a new one.
    
    try:
        await callback.message.delete()
    except:
        pass
        
    if news.image_file_id:
        await callback.message.answer_photo(
            photo=news.image_file_id,
            caption=text,
            reply_markup=reply_markup
        )
    else:
        await callback.message.answer(
            text=text,
            reply_markup=reply_markup
        )
