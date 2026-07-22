import csv

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
# async def get_all_heroes_by_type(hero_type: str = Query(min_length=3, max_length=20)):
#     result = []
#     for hero in HEROES:
#         if hero_type.casefold() in hero.type.casefold():
#             result.append(hero)
#     return result

async def get_all_heroes_by_type(db: db_dependency, hero_type: str = Query(min_length=3, max_length=20)):
    result = db.query(Heroes).filter(Heroes.type.ilike(f"%{hero_type}%")).order_by(Heroes.id.asc()).all()
    return result



#Get by rank (as QUERY PARAM)
@app.get("/heroes/rank", status_code=status.HTTP_200_OK )
async def get_all_heroes_by_rank(db: db_dependency, hero_rank: int = Query(ge=0,le=100)):
    result = db.query(Heroes).filter(Heroes.rank >= hero_rank).order_by(Heroes.rank.asc()).all()
    return result
    # result = []
    # for hero in HEROES:
    #     if hero.rank >= hero_rank:
    #         result.append(hero)
    # return result

#Get by id (as PATH PARAM, not query)
@app.get("/hero/id/{hero_id}")
async def get_one_hero_by_id(db: db_dependency, hero_id: int = Path(gt=0)):
    hero_db = db.query(Heroes).filter(Heroes.id == hero_id).first()
    if hero_db is not None:
        return hero_db
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Hero not found"})
    

# async def get_one_hero_by_id(hero_id: int = Path(gt=0)):
#     for hero in HEROES:
#         if hero.id == hero_id:
#             return hero
#         else:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Hero not found"})

# @app.get("/heroes/id")
# async def get_hero_by_id(hero_id: int = Query()):
#     result = []
#     for hero in HEROES:
#         if hero.get("id") == hero_id:
#             result.append(hero)
#     return result

#Get one hero by nickname (as PATH PARAM)
@app.get("/hero/nick/{nick}",status_code=status.HTTP_200_OK)
async def get_one_hero_by_nick(db : db_dependency, nick: str = Path()):
    result = db.query(Heroes).filter(Heroes.nick_name.ilike(f"%{nick}%")).all()
    return result

    #  for hero in HEROES:
    #     if nick.casefold() in hero.nick_name.casefold():
    #          return hero
    #     else:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Nickname not found"})

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
async def create_hero(db : db_dependency, hero_body: HeroValidation = Body(),status_code=status.HTTP_201_CREATED):
    #new_hero = Hero(**hero_body.model_dump())
    new_hero = Heroes(**hero_body.model_dump(exclude={"id"}))  # Exclude the 'id' field when creating a new hero
    db.add(new_hero)
    db.commit()
    # print(type(new_hero))
    # HEROES.append(find_proper_hero_id(new_hero))
    # #pass

# UPDATE WITH PUT (BY BODY)
# @app.put("/hero/update", status_code=status.HTTP_204_NO_CONTENT)
# async def update_hero(hero_body: HeroValidation = Body()): #utilisation de HeroValidation -> même description swagger
#     hero_changed = False
#     for i in range(len(HEROES)):
#         if HEROES[i].id == hero_body.id:
#             hero_changed = True
#             HEROES[i] = Hero(**hero_body.model_dump())
#         if not hero_changed:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Hero not found"})


# UPDATE WITH PUT (BY PATH)
@app.put("/hero/update/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_hero(db : db_dependency, hero_id: int = Path(), hero_body: HeroValidation = Body()): #utilisation de HeroValidation -> même description swagger
    
    hero_db = db.query(Heroes).filter(Heroes.id == hero_id).first()

    if  hero_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Hero not found"})
    else:
        hero_db.nick_name = hero_body.nick_name
        hero_db.full_name = hero_body.full_name
        hero_db.occupation = hero_body.occupation
        hero_db.powers = hero_body.powers
        hero_db.hobby = hero_body.hobby
        hero_db.type = hero_body.type
        hero_db.rank = hero_body.rank
        db.add(hero_db)

        db.commit()


# #Delete by id (as PATH PARAM, not query)
# @app.delete("/hero/delete/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_hero(hero_id: int = Path()):
#     hero_changed = False
#     for i in range(len(HEROES)):
#         if HEROES[i].id == hero_id:
#             hero_changed = True
#             HEROES.pop(i)
#             break
#         if not hero_changed:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Hero not found, therefore cannot be deleted"})


# Delete by id (as PATH PARAM)
@app.delete("/hero/delete/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hero(db : db_dependency, hero_id: int = Path(gt=0)):
    hero_db = db.query(Heroes).filter(Heroes.id == hero_id).first()

    if  hero_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Hero not found, therefore cannot be deleted"})
    else:
        db.delete(hero_db)
        db.commit()





# CREATE A CSV FILE FROM THE ABOVE
def format_array(py_list):
    return '{' + ','.join([f'"{item}"' for item in py_list]) + '}'
    # csv_string = ""
    # for hero in py_list:
    #     csv_string += f"{hero.id},{hero.nick_name},{hero.type},{hero.rank}\n"
    # return csv_string

with open("heroes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    # HEADERS
    writer.writerow(["id", "nick_name", "type", "rank"])
    for hero in HEROES:
        writer.writerow([hero.nick_name, hero.full_name, \
                         format_array(hero.occupation), format_array(hero.powers), \
                         format_array(hero.hobby), hero.type,hero.rank])    

