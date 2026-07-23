from fastapi import APIRouter, Body
from classes import PlayerValidation

router = APIRouter()

@router.post("/auth/register")
async def register_player(player_body: PlayerValidation = Body()):
    return {"message": "Player registered successfully", "player": player_body}