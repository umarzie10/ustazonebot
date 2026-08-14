from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from aiogram.fsm.storage.redis import RedisStorage
from bot.loader import storage

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 1):
        self.limit = limit
        self.storage: RedisStorage = storage

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        user_id = event.from_user.id
        redis = self.storage.redis
        
        # Simple token bucket or rate limit logic using Redis
        key = f"throttle_{user_id}"
        val = await redis.get(key)
        
        if val:
            return # Throttled, ignore message
        
        await redis.setex(key, self.limit, 1)
        return await handler(event, data)
