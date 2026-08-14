from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from bot.config import config
from typing import Sequence
from bot.database.models import Faq
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="🌐 Saytni ochish", web_app=WebAppInfo(url=config.webapp_url), style="primary")],
        [InlineKeyboardButton(text="✉️ Xabar yozish", callback_data="write_message", style="primary")],
        [InlineKeyboardButton(text="📰 Ustazone Yangiliklari", url="https://t.me/ustazone_uz", style="primary")],
        [
            InlineKeyboardButton(text="❓ FAQ", callback_data="faq_menu", style="primary"),
            InlineKeyboardButton(text="ℹ️ Haqida", callback_data="about", style="primary")
        ],
        [InlineKeyboardButton(text="📱 Ijtimoiy tarmoqlar", callback_data="socials", style="primary")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_socials_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Telegram", url=config.social_telegram, style="primary")
        ],
        [
            InlineKeyboardButton(text="YouTube", url=config.social_youtube, style="primary"),
            InlineKeyboardButton(text="TikTok", url=config.social_tiktok, style="primary")
        ],
        [InlineKeyboardButton(text="Website", url=config.webapp_url, style="primary")],
        [InlineKeyboardButton(text="⬅️ Ortga", callback_data="main_menu", style="primary")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_faq_menu(faqs: Sequence[Faq]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for faq in faqs:
        builder.button(text=faq.question, callback_data=f"faq_item_{faq.id}", style="primary")
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="⬅️ Ortga", callback_data="main_menu", style="primary"))
    return builder.as_markup()

def get_faq_back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Ortga", callback_data="faq_menu", style="primary")]
    ])

def get_news_pagination(page: int, total: int) -> InlineKeyboardMarkup:
    buttons = []
    if page > 0:
        buttons.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"news_page_{page-1}", style="primary"))
    if page < total - 1:
        buttons.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"news_page_{page+1}", style="primary"))
        
    builder = InlineKeyboardBuilder()
    if buttons:
        builder.row(*buttons)
    builder.row(InlineKeyboardButton(text="⬅️ Ortga", callback_data="main_menu", style="primary"))
    return builder.as_markup()

def get_about_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Saytni ochish", web_app=WebAppInfo(url=config.webapp_url), style="primary")],
        [InlineKeyboardButton(text="⬅️ Ortga", callback_data="main_menu", style="primary")]
    ])

def get_admin_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats", style="primary")],
        [InlineKeyboardButton(text="📢 Broadcast", callback_data="admin_broadcast", style="primary")],
        [
            InlineKeyboardButton(text="➕ Yangilik qo'shish", callback_data="admin_add_news", style="success"),
            InlineKeyboardButton(text="🗑 Yangilik o'chirish", callback_data="admin_del_news", style="danger")
        ],
        [InlineKeyboardButton(text="⬅️ Chiqish", callback_data="main_menu", style="danger")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_message_categories_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="💬 Admin bilan bog'lanish", callback_data="msg_cat_admin", style="primary")],
        [InlineKeyboardButton(text="🛠 Muammo haqida xabar", callback_data="msg_cat_problem", style="primary")],
        [InlineKeyboardButton(text="💡 Taklif yuborish", callback_data="msg_cat_suggestion", style="primary")],
        [InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="main_menu", style="primary")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
