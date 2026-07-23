from fastapi import FastAPI
from database import db_dependency, engine
from routers import auth_router, heroes_router

import models
import csv

app = FastAPI()

import models


models.Base.metadata.create_all(bind=engine)  # Create tables in the database

app.include_router(heroes_router.router)
app.include_router(auth_router.router)

print(models.__file__)
print(models.Base.metadata.tables.keys())