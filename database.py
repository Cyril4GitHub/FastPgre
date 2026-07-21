from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends
from typing import Annotated

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/dbfast'

# DEF ENGINE
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

# DEF SESSION
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DEF of base as an object, for inheritance
Base = declarative_base()

# DEPENDENCY CORE
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# DEPENDENCY ANNOTATED
db_dependency = Annotated[Session, Depends(get_db)]

