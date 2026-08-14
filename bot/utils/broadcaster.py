import asyncio
import logging
from typing import List
from aiogram import Bot
from aiogram.types import Message
from aiogram.exceptions import TelegramRetryAfter

logger = logging.getLogger(__name__)

async def send_message_with_retry(bot: Bot, user_id: int, message: Message) -> bool:
    try:
        await bot.copy_message(
            chat_id=user_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        return True
    except TelegramRetryAfter as e:
        logger.warning(f"Flood limit exceeded. Retry after {e.retry_after} seconds.")
        await asyncio.sleep(e.retry_after)
        return await send_message_with_retry(bot, user_id, message)
    except Exception as e:
        logger.error(f"Failed to send message to {user_id}: {e}")
        return False

async def broadcast(bot: Bot, user_ids: List[int], message: Message):
    success_count = 0
    fail_count = 0
    
    for i, user_id in enumerate(user_ids):
        # Prevent flood limit, sleep 1 second for every 30 messages (Telegram limit is ~30 msgs/sec for broadcasting)
        if i > 0 and i % 30 == 0:
            await asyncio.sleep(1)
            
        success = await send_message_with_retry(bot, user_id, message)
        if success:
            success_count += 1
        else:
            fail_count += 1
            
    try:
        await message.reply(f"📣 Broadcast yakunlandi.\n\nMuvaffaqiyatli: {success_count}\nXatolik: {fail_count}")
    except:
        pass
