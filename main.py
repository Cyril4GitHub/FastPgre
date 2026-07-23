from fastapi import FastAPI
from database import db_dependency, engine
from routers import heroes_router

import models
import csv

app = FastAPI()


models.Base.metadata.create_all(bind=engine)  # Create tables in the database

app.include_router(heroes_router.router)