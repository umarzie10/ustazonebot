from typing import Sequence, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models import Faq

async def get_all_faqs(session: AsyncSession) -> Sequence[Faq]:
    result = await session.execute(select(Faq))
    return result.scalars().all()

async def get_faq_by_id(session: AsyncSession, faq_id: int) -> Optional[Faq]:
    return await session.get(Faq, faq_id)

async def create_faq(session: AsyncSession, question: str, answer: str) -> Faq:
    faq = Faq(question=question, answer=answer)
    session.add(faq)
    await session.commit()
    return faq
