from typing import Optional, Sequence
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import News

async def get_news_count(session: AsyncSession) -> int:
    result = await session.execute(select(func.count(News.id)))
    return result.scalar_one()

async def get_news_paginated(session: AsyncSession, offset: int, limit: int = 1) -> Sequence[News]:
    result = await session.execute(
        select(News).order_by(News.created_at.desc()).offset(offset).limit(limit)
    )
    return result.scalars().all()

async def create_news(session: AsyncSession, title: str, text: str, image_file_id: Optional[str] = None) -> News:
    news = News(title=title, text=text, image_file_id=image_file_id)
    session.add(news)
    await session.commit()
    return news

async def delete_news(session: AsyncSession, news_id: int) -> bool:
    news = await session.get(News, news_id)
    if news:
        await session.delete(news)
        await session.commit()
        return True
    return False
