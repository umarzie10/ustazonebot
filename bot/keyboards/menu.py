from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from bot.config import config
from typing import Sequence
from bot.database.models import Faq
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="🌐 Saytni ochish", url=config.webapp_url, style="primary")],
        [InlineKeyboardButton(text="✉️ Xabar yozish", callback_data="write_message", style="success")],
        [InlineKeyboardButton(text="📢 Yangiliklar", url="https://t.me/ustazone_uz", style="primary")],
        [
            InlineKeyboardButton(text="❓ Yordam", callback_data="faq_menu", style="primary"),
            InlineKeyboardButton(text="ℹ️ Haqida", callback_data="about", style="primary")
        ],
        [InlineKeyboardButton(text="📱 Ijtimoiy tarmoqlar", callback_data="socials", style="primary")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_socials_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✈️ Telegram", url="https://t.me/ustazone_uz", style="primary"))
    if config.social_youtube:
        builder.row(InlineKeyboardButton(text="▶️ YouTube", url=config.social_youtube, style="primary"))
    if config.social_tiktok:
        builder.row(InlineKeyboardButton(text="🎵 TikTok", url=config.social_tiktok, style="primary"))
    builder.row(InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu", style="primary"))
    return builder.as_markup()

def get_yordam_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="🔎 Usta qanday topiladi?", callback_data="faq_find", style="primary")],
        [InlineKeyboardButton(text="📋 Buyurtma qanday beriladi?", callback_data="faq_order", style="primary")],
        [InlineKeyboardButton(text="💳 To‘lov qanday ishlaydi?", callback_data="faq_payment", style="primary")],
        [InlineKeyboardButton(text="⭐ Reyting qanday beriladi?", callback_data="faq_rating", style="primary")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu", style="primary")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_yordam_back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="faq_menu", style="primary")]
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
    builder.row(InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu", style="primary"))
    return builder.as_markup()

def get_about_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 Saytni ochish", url=config.webapp_url, style="primary")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu", style="primary")]
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

def get_contact_operator_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Operatorga yozish", callback_data="msg_cat_admin", style="primary")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu", style="primary")]
    ])
