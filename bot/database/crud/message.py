from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import Message

async def save_message(session: AsyncSession, user_id: int, message_id: int, text: str | None = None) -> Message:
    message = Message(user_id=user_id, message_id=message_id, text=text)
    session.add(message)
    await session.commit()
    return message
