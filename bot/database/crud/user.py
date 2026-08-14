from typing import Optional, Sequence
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import User

async def get_user(session: AsyncSession, user_id: int) -> Optional[User]:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def create_user(session: AsyncSession, user_id: int, full_name: str, username: Optional[str]) -> User:
    user = User(id=user_id, full_name=full_name, username=username)
    session.add(user)
    await session.commit()
    return user

async def count_users(session: AsyncSession) -> int:
    result = await session.execute(select(func.count(User.id)))
    return result.scalar_one()

async def count_users_today(session: AsyncSession) -> int:
    result = await session.execute(
        select(func.count(User.id)).where(func.date(User.created_at) == func.current_date())
    )
    return result.scalar_one()

async def get_all_users(session: AsyncSession) -> Sequence[User]:
    result = await session.execute(select(User))
    return result.scalars().all()
