from database import Base

from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import ARRAY


class Heroes(Base):
    __tablename__ = "heroes"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    nick_name = Column(String(50), primary_key=False, index=False)
    full_name = Column(String(50), primary_key=False, index=False)
    occupation = Column(ARRAY(String(50)), primary_key=False, index=False) #List[Str]
    powers = Column(ARRAY(String(50)), primary_key=False, index=False)
    hobby = Column(ARRAY(String(50)), primary_key=False, index=False)
    type = Column(String(50), primary_key=False, index=False)
    rank = Column(Integer, primary_key=False, index=False)

