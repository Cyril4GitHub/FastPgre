# from database import Base

# from sqlalchemy import Column, String, Integer
# from sqlalchemy.dialects.postgresql import ARRAY


# class Heroes(Base):
#     __tablename__ = "heroes"

#     id = Column(Integer, autoincrement=True, primary_key=True, index=True)
#     nick_name = Column(String(50), primary_key=False, index=False)
#     full_name = Column(String(50), primary_key=False, index=False)
#     occupation = Column(ARRAY(String(50)), primary_key=False, index=False) #List[Str]
#     powers = Column(ARRAY(String(50)), primary_key=False, index=False)
#     hobby = Column(ARRAY(String(50)), primary_key=False, index=False)
#     type = Column(String(50), primary_key=False, index=False)
#     rank = Column(Integer, primary_key=False, index=False)

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