from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Faq(Base):
    __tablename__ = "faq"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
