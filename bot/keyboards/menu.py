from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from bot.config import config
from typing import Sequence
from bot.database.models import Faq
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="🌐 Saytni ochish", web_app=WebAppInfo(url=config.webapp_url))],
        [InlineKeyboardButton(text="✉️ Xabar yozish", callback_data="write_message")],
        [InlineKeyboardButton(text="📰 Ustazone Yangiliklari", url="https://t.me/ustazone_uz")],
        [
            InlineKeyboardButton(text="❓ FAQ", callback_data="faq_menu"),
            InlineKeyboardButton(text="ℹ️ Haqida", callback_data="about")
        ],
        [InlineKeyboardButton(text="📱 Ijtimoiy tarmoqlar", callback_data="socials")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_socials_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Telegram", url=config.social_telegram)
        ],
        [
            InlineKeyboardButton(text="YouTube", url=config.social_youtube),
            InlineKeyboardButton(text="TikTok", url=config.social_tiktok)
        ],
        [InlineKeyboardButton(text="Website", url=config.webapp_url)],
        [InlineKeyboardButton(text="⬅️ Ortga", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_faq_menu(faqs: Sequence[Faq]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for faq in faqs:
        builder.button(text=faq.question, callback_data=f"faq_item_{faq.id}")
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="⬅️ Ortga", callback_data="main_menu"))
    return builder.as_markup()

def get_faq_back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Ortga", callback_data="faq_menu")]
    ])

def get_news_pagination(page: int, total: int) -> InlineKeyboardMarkup:
    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"news_page_{page-1}"))
    if page < total - 1:
        buttons.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"news_page_{page+1}"))
        
    builder = InlineKeyboardBuilder()
    if buttons:
        builder.row(*buttons)
    builder.row(InlineKeyboardButton(text="⬅️ Ortga", callback_data="main_menu"))
    return builder.as_markup()

def get_about_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Saytni ochish", web_app=WebAppInfo(url=config.webapp_url))],
        [InlineKeyboardButton(text="⬅️ Ortga", callback_data="main_menu")]
    ])

def get_admin_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats")],
        [InlineKeyboardButton(text="📢 Broadcast", callback_data="admin_broadcast")],
        [
            InlineKeyboardButton(text="➕ Yangilik qo'shish", callback_data="admin_add_news"),
            InlineKeyboardButton(text="🗑 Yangilik o'chirish", callback_data="admin_del_news")
        ],
        [InlineKeyboardButton(text="⬅️ Chiqish", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_message_categories_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="💬 Admin bilan bog'lanish", callback_data="msg_cat_admin")],
        [InlineKeyboardButton(text="🛠 Muammo haqida xabar", callback_data="msg_cat_problem")],
        [InlineKeyboardButton(text="💡 Taklif yuborish", callback_data="msg_cat_suggestion")],
        [InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
