from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import config
from bot.database.crud.user import count_users, count_users_today, get_all_users
from bot.database.crud.news import create_news, delete_news
from bot.keyboards.menu import get_admin_menu
from bot.utils.broadcaster import broadcast

router = Router()

ADMIN_ID = 6265790648  # Hardcoded fallback

def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID or user_id == config.admin_id

router.message.filter(lambda m: is_admin(m.from_user.id))
router.callback_query.filter(lambda c: is_admin(c.from_user.id))

class AdminStates(StatesGroup):
    waiting_for_news_title = State()
    waiting_for_news_text = State()
    waiting_for_news_image = State()
    
    waiting_for_del_news_id = State()
    waiting_for_broadcast = State()

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    await message.answer("🛠 Admin panelga xush kelibsiz", reply_markup=get_admin_menu())

@router.callback_query(F.data == "admin_stats")
async def cq_admin_stats(callback: CallbackQuery, session: AsyncSession):
    total = await count_users(session)
    today = await count_users_today(session)
    users = await get_all_users(session)
    
    user_list = ""
    for i, u in enumerate(users[-30:], 1):  # oxirgi 30 ta foydalanuvchi
        username = f"@{u.username}" if u.username else u.full_name
        user_list += f"\n{i}. {username} (<code>{u.id}</code>)"
    
    text = (
        f"📊 <b>Statistika</b>\n\n"
        f"Jami foydalanuvchilar: <b>{total}</b>\n"
        f"Bugungi: <b>{today}</b>\n\n"
        f"<b>Foydalanuvchilar ro'yxati:</b>{user_list if user_list else '\nHali hech kim yo\'q'}"
    )
    await callback.message.edit_text(text, reply_markup=get_admin_menu(), parse_mode="HTML")

@router.callback_query(F.data == "admin_add_news")
async def cq_admin_add_news(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Yangilik sarlavhasini yuboring:")
    await state.set_state(AdminStates.waiting_for_news_title)

@router.message(AdminStates.waiting_for_news_title)
async def admin_news_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Yangilik matnini yuboring:")
    await state.set_state(AdminStates.waiting_for_news_text)

@router.message(AdminStates.waiting_for_news_text)
async def admin_news_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer("Rasm yuboring (Yoki 'skip' deb yozing):")
    await state.set_state(AdminStates.waiting_for_news_image)

@router.message(AdminStates.waiting_for_news_image)
async def admin_news_image(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    title = data['title']
    text = data['text']
    
    image_file_id = None
    if message.photo:
        image_file_id = message.photo[-1].file_id
        
    await create_news(session, title, text, image_file_id)
    await message.answer("✅ Yangilik qo'shildi", reply_markup=get_admin_menu())
    await state.clear()

@router.callback_query(F.data == "admin_del_news")
async def cq_admin_del_news(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("O'chirilishi kerak bo'lgan yangilik ID sini yuboring:")
    await state.set_state(AdminStates.waiting_for_del_news_id)

@router.message(AdminStates.waiting_for_del_news_id)
async def admin_del_news_id(message: Message, state: FSMContext, session: AsyncSession):
    try:
        news_id = int(message.text)
        deleted = await delete_news(session, news_id)
        if deleted:
            await message.answer("✅ O'chirildi")
        else:
            await message.answer("❌ Topilmadi")
    except ValueError:
        await message.answer("Faqat raqam yuboring")
    finally:
        await state.clear()

@router.callback_query(F.data == "admin_broadcast")
async def cq_admin_broadcast(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Barcha foydalanuvchilarga yuboriladigan xabarni yuboring:")
    await state.set_state(AdminStates.waiting_for_broadcast)

@router.message(AdminStates.waiting_for_broadcast)
async def admin_broadcast(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    users = await get_all_users(session)
    user_ids = [u.id for u in users]
    
    await message.answer("Broadcast boshlandi...")
    await state.clear()
    
    await broadcast(bot, user_ids, message)
