from database import Base

from sqlalchemy import String, Integer
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column


class Heroes(Base):
    __tablename__ = "heroes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    nick_name: Mapped[str] = mapped_column(String(50))
    full_name: Mapped[str] = mapped_column(String(50))
    occupation: Mapped[list[str]] = mapped_column(ARRAY(String(50)))
    powers: Mapped[list[str]] = mapped_column(ARRAY(String(50)))
    hobby: Mapped[list[str]] = mapped_column(ARRAY(String(50)))
    type: Mapped[str] = mapped_column(String(50))
    rank: Mapped[int] = mapped_column(Integer)