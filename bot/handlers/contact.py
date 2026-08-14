from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import config
from bot.database.crud.message import save_message
from bot.keyboards.menu import get_main_menu, get_message_categories_menu

router = Router()

class ContactState(StatesGroup):
    waiting_for_message = State()

@router.callback_query(F.data == "write_message")
async def cq_write_message(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "Qaysi bo'limga xabar yozmoqchisiz? Kategoriyani tanlang:",
        reply_markup=get_message_categories_menu()
    )

@router.callback_query(F.data.startswith("msg_cat_"))
async def cq_msg_category(callback: CallbackQuery, state: FSMContext):
    category = callback.data.split("_")[2]
    await state.update_data(msg_category=category)
    
    await callback.message.edit_text(
        "✍️ Xabaringizni yuboring.\nOperatorlarimiz sizga tez orada javob berishadi.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Ortga", callback_data="write_message", style="primary")]
        ])
    )
    await state.set_state(ContactState.waiting_for_message)

@router.message(ContactState.waiting_for_message)
async def msg_from_user(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    if not message.text and not message.photo and not message.video:
        await message.answer("Iltimos, matn, rasm yoki video yuboring.")
        return
        
    data = await state.get_data()
    category = data.get("msg_category", "admin")
    
    cat_names = {
        "admin": "💬 Admin bilan bog'lanish",
        "problem": "🛠 Muammo haqida xabar",
        "suggestion": "💡 Taklif yuborish"
    }
    cat_name = cat_names.get(category, "Xabar")

    # Send category info to admin first
    await bot.send_message(
        chat_id=config.admin_chat_id,
        text=f"📨 <b>Yangi xabar keldi!</b>\n\n📌 <b>Kategoriya:</b> {cat_name}\n👤 <b>Foydalanuvchi:</b> {message.from_user.full_name} (@{message.from_user.username or 'yoq'})\n🆔 <b>ID:</b> <code>{message.from_user.id}</code>",
        parse_mode="HTML"
    )

    # Forward to admin
    fwd = await message.forward(chat_id=config.admin_chat_id)
    
    # Save to db
    await save_message(
        session=session,
        user_id=message.from_user.id,
        message_id=fwd.message_id,
        text=message.text or message.caption or "Media xabar"
    )
    
    await message.answer("✅ Xabaringiz yuborildi. Tez orada javob qaytaramiz.", reply_markup=get_main_menu())
    await state.clear()

# Admin reply handler
@router.message(
    F.chat.id == config.admin_chat_id,
    F.reply_to_message,
    F.reply_to_message.forward_from
)
async def msg_from_admin(message: Message, bot: Bot):
    original_user_id = message.reply_to_message.forward_from.id
    try:
        await bot.copy_message(
            chat_id=original_user_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        await message.react([{"type": "emoji", "emoji": "👍"}])
    except Exception as e:
        await message.reply(f"Xatolik: {e}")
