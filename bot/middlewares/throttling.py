from typing import Any, Awaitable, Callable, Dict
import time
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from bot.loader import storage

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 1):
        self.limit = limit
        self.storage = storage
        self.cache = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        user_id = event.from_user.id
        
        if hasattr(self.storage, 'redis'):
            redis = self.storage.redis
            key = f"throttle_{user_id}"
            val = await redis.get(key)
            if val:
                return
            await redis.setex(key, self.limit, 1)
        else:
            now = time.time()
            last_time = self.cache.get(user_id, 0)
            if now - last_time < self.limit:
                return
            self.cache[user_id] = now
            
        return await handler(event, data)
