from fastapi import FastAPI, Query, Path, Body

from heroes import HEROES

from utils import find_proper_hero_id


app = FastAPI()

# Get server status
@app.get("/")
async def heartbeat():
    return "App running"

# Get All heroes
@app.get("/heroes")
async def get_all_heroes():
    return HEROES

#Get by type (as QUERY PARAM)
@app.get("/heroes/type")
async def get_all_heroes_by_type(hero_type: str = Query()):
    result = []
    for hero in HEROES:
        if hero_type.casefold() in hero.get("type").casefold():
            result.append(hero)
    return result

#Get by rank (as QUERY PARAM)
@app.get("/heroes/rank")
async def get_all_heroes_by_rank(hero_rank: int = Query()):
    result = []
    for hero in HEROES:
        if hero.get("rank") >= hero_rank:
            result.append(hero)
    return result

#Get by id (as PATH PARAM, not query)
@app.get("/hero/id/{hero_id}")
async def get_one_hero_by_id(hero_id: int = Path()):
    for hero in HEROES:
        if hero.get("id") == hero_id:
            return hero

# @app.get("/heroes/id")
# async def get_hero_by_id(hero_id: int = Query()):
#     result = []
#     for hero in HEROES:
#         if hero.get("id") == hero_id:
#             result.append(hero)
#     return result

#Get one hero by nickname (as PATH PARAM)
@app.get("/hero/nick/{nick}")
async def get_one_hero_by_nick(nick: str = Path()):
     for hero in HEROES:
         if nick.casefold() in hero.get("nick_name").casefold():
             return hero

# POST/CREATE (BY BODY)
@app.post("/hero/create")
async def create_hero(hero_body = Body()):
    HEROES.append(find_proper_hero_id(hero_body))

# UPDATE WITH PUT (BY BODY)
@app.put("/hero/update")
async def update_hero(hero_body = Body()):
    for i in range(len(HEROES)):
        if HEROES[i].get("id") == hero_body.get("id"):
            HEROES[i] = hero_body

#Delete by id (as PATH PARAM, not query)
@app.delete("/hero/delete/{hero_id}")
async def delete_hero(hero_id: int = Path()):
    for i in range(len(HEROES)):
        if HEROES[i].get("id") == hero_id:
            HEROES.pop(i)
            break
