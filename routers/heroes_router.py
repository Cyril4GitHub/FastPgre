import csv
from typing import Annotated

from fastapi import HTTPException, Query, Path, Body, APIRouter, Depends

from classes import HeroValidation
from starlette import status


from database import db_dependency, engine
from sqlalchemy import text

import models
from models import Heroes

from routers.auth_router import get_current_player


router = APIRouter(
    tags=["Heroes"],
    prefix="/heroes"
)

#DEPENDENCIES
player_dependency = Annotated[dict, Depends(get_current_player)]

models.Base.metadata.create_all(bind=engine)  # Create tables in the database


# Get server status
@router.get("/heartbeat")
async def heartbeat(db : db_dependency):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "DATABASE Ok"}
    except Exception as e:
        return { "error":str(e) }
    

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_heroes(db: db_dependency):
    return db.query(Heroes).order_by(Heroes.id.asc()).all()


#Get by type (as QUERY PARAM)
@router.get("/type", status_code=status.HTTP_200_OK)
async def get_all_heroes_by_type(db: db_dependency, hero_type: str = Query(min_length=3, max_length=20)):
    result = db.query(Heroes).filter(Heroes.type.ilike(f"%{hero_type}%")).order_by(Heroes.id.asc()).all()
    return result


#Get by rank (as QUERY PARAM)
@router.get("/rank", status_code=status.HTTP_200_OK )
async def get_all_heroes_by_rank(db: db_dependency, hero_rank: int = Query(ge=0,le=100)):
    result = db.query(Heroes).filter(Heroes.rank >= hero_rank).order_by(Heroes.rank.asc()).all()
    return result


#Get by id (as PATH PARAM, not query)
@router.get("/id/{hero_id}")
async def get_one_hero_by_id(db: db_dependency, hero_id: int = Path(gt=0)):
    hero_db = db.query(Heroes).filter(Heroes.id == hero_id).first()
    if hero_db is not None:
        return hero_db
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Hero not found"})


#Get one hero by nickname (as PATH PARAM)
@router.get("/nick/{nick}",status_code=status.HTTP_200_OK)
async def get_one_hero_by_nick(db : db_dependency, nick: str = Path()):
    result = db.query(Heroes).filter(Heroes.nick_name.ilike(f"%{nick}%")).all()
    return result


# POST/CREATE (BY BODY)
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_hero(player: player_dependency, db: db_dependency, hero_body: HeroValidation = Body()):
    if player is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized - Invalid token")
    new_hero = Heroes(**hero_body.model_dump(exclude={"id"}), owner_id=player["id"])  # Exclude the 'id' field when creating a new hero
    db.add(new_hero)
    db.commit()
    db.refresh(new_hero)
    return new_hero


# UPDATE WITH PUT (BY PATH)
@router.put("/update/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
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


# Delete by id (as PATH PARAM)
@router.delete("/delete/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hero(db : db_dependency, hero_id: int = Path(gt=0)):
    hero_db = db.query(Heroes).filter(Heroes.id == hero_id).first()

    if  hero_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Hero not found, therefore cannot be deleted"})
    else:
        db.delete(hero_db)
        db.commit()



# # CREATE A CSV FILE FROM THE ABOVE
# def format_array(py_list):
#     return '{' + ','.join([f'"{item}"' for item in py_list]) + '}'

# with open("heroes.csv", "w", newline="", encoding="utf-8") as f:
#     writer = csv.writer(f)
#     # HEADERS
#     writer.writerow(["id", "nick_name", "type", "rank"])
#     for hero in HEROES:
#         writer.writerow([hero.nick_name, hero.full_name, \
#                          format_array(hero.occupation), format_array(hero.powers), \
#                          format_array(hero.hobby), hero.type,hero.rank])    

