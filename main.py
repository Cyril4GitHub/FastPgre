from fastapi import FastAPI

from heroes import HEROES

app = FastAPI()

# Get server status
@app.get("/")
async def heartbeat():
    return "App running"

# Get All heroes
@app.get("/heroes")
async def get_all_heroes():
    return HEROES