from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from bot.database.engine import async_session
from bot.database.crud.user import get_user, create_user

class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        # We need to extract the user from event
        user = None
        if hasattr(event, "from_user") and event.from_user:
            user = event.from_user
        elif hasattr(event, "message") and event.message and event.message.from_user:
            user = event.message.from_user
        elif hasattr(event, "callback_query") and event.callback_query and event.callback_query.from_user:
            user = event.callback_query.from_user
            
        if user and not user.is_bot:
            async with async_session() as session:
                db_user = await get_user(session, user.id)
                if not db_user:
                    db_user = await create_user(
                        session=session,
                        user_id=user.id,
                        full_name=user.full_name,
                        username=user.username
                    )
                data["db_user"] = db_user
                data["session"] = session

                return await handler(event, data)
        
        # If no user or is bot, just pass empty session or don't attach db_user
        async with async_session() as session:
            data["session"] = session
            return await handler(event, data)
