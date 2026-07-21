from fastapi import FastAPI, HTTPException, Query, Path, Body
from heroes import HEROES
from classes import Hero, HeroValidation
from starlette import status
from utils import find_proper_hero_id

from database import db_dependency, engine
from sqlalchemy import text

import models
from models import Heroes

app = FastAPI()


models.Base.metadata.create_all(bind=engine)  # Create tables in the database

# Get server status
# @app.get("/")
# async def heartbeat():
#     return "App running"

# Get server status
@app.get("/")
async def heartbeat(db : db_dependency):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "DATABASE Ok"}
    except Exception as e:
        return { "error":str(e) }
    
# Get All heroes
#@app.get("/heroes", status_code=status.HTTP_200_OK)
# async def get_all_heroes():
#     return HEROES
@app.get("/heroes", status_code=status.HTTP_200_OK)
async def get_all_heroes(db: db_dependency):
    return db.query(Heroes).order_by(Heroes.id.asc()).all()



#Get by type (as QUERY PARAM)
@app.get("/heroes/type", status_code=status.HTTP_200_OK)
async def get_all_heroes_by_type(hero_type: str = Query(min_length=3, max_length=20)):
    result = []
    for hero in HEROES:
        if hero_type.casefold() in hero.type.casefold():
            result.append(hero)
    return result

#Get by rank (as QUERY PARAM)
@app.get("/heroes/rank", status_code=status.HTTP_200_OK )
async def get_all_heroes_by_rank(hero_rank: int = Query(ge=0,le=100)):
    result = []
    for hero in HEROES:
        if hero.rank >= hero_rank:
            result.append(hero)
    return result

#Get by id (as PATH PARAM, not query)
@app.get("/hero/id/{hero_id}")
async def get_one_hero_by_id(hero_id: int = Path(gt=0)):
    for hero in HEROES:
        if hero.id == hero_id:
            return hero
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Hero not found"})

# @app.get("/heroes/id")
# async def get_hero_by_id(hero_id: int = Query()):
#     result = []
#     for hero in HEROES:
#         if hero.get("id") == hero_id:
#             result.append(hero)
#     return result

#Get one hero by nickname (as PATH PARAM)
@app.get("/hero/nick/{nick}")
async def get_one_hero_by_nick(nick: str = Path(gt=0)):
     for hero in HEROES:
        if nick.casefold() in hero.nick_name.casefold():
             return hero
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Nickname not found"})


# # POST/CREATE (BY BODY)
# @app.post("/hero/create")
# async def create_hero(hero_body = Body()):
#     HEROES.append(find_proper_hero_id(hero_body))

# # POST/CREATE (BY BODY)
# @app.post("/hero/create")
# async def create_hero(hero_body: HeroValidation = Body()):
#     print(type(hero_body))
#     pass

# POST/CREATE (BY BODY)
@app.post("/hero/create")
async def create_hero(hero_body: HeroValidation = Body(),status_code=status.HTTP_201_CREATED):
    new_hero = Hero(**hero_body.model_dump())
    print(type(new_hero))
    HEROES.append(find_proper_hero_id(new_hero))
    #pass

# UPDATE WITH PUT (BY BODY)
@app.put("/hero/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_hero(hero_body: HeroValidation = Body()): #utilisation de HeroValidation -> même description swagger
    hero_changed = False
    for i in range(len(HEROES)):
        if HEROES[i].id == hero_body.id:
            hero_changed = True
            HEROES[i] = Hero(**hero_body.model_dump())
        if not hero_changed:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Hero not found"})


#Delete by id (as PATH PARAM, not query)
@app.delete("/hero/delete/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hero(hero_id: int = Path()):
    hero_changed = False
    for i in range(len(HEROES)):
        if HEROES[i].id == hero_id:
            hero_changed = True
            HEROES.pop(i)
            break
        if not hero_changed:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Hero not found, therefore cannot be deleted"})
