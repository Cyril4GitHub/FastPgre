from typing import Annotated
from fastapi import APIRouter, Body, Depends
from starlette import status
from classes import PlayerValidation
from models import Players
from database import db_dependency
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta, timezone

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT_CONFIG
# KEY GENERATED WITH COMMAND: openssl rand -hex 64
JWT_SECRET_KEY = "16c914db5643557bce0ef699088b8197381e0285744a5f5622a391176865bc1c9f4d66d119b8ed7d9053445ed6024833a90e836f1801617b06fd67ed78278371"
JWT_ALGO = "HS256"


# HELPER FUNCTION FOR LOGIN
def authenticate_player(db, username: str, password: str):
    print(f"Username reçu : '{username}'")
    found_player = db.query(Players).filter(Players.username == username).first()
    for p in db.query(Players).all():
        print(p.id, p.username)

    if  not found_player or not bcrypt_context.verify(password, found_player.hashed_password):
        print(f"Found player: {found_player}")
        print("Invalid username or password")
        return None
    else:
        return found_player


def create_token(username: str, user_id: int, expires_delta: timedelta = None):
    encoded_data = {"sub": username, "id": user_id}
    expiration = datetime.now(timezone.utc) + (expires_delta)
    encoded_data.update({"exp": expiration.timestamp()})
    return jwt.encode(encoded_data, JWT_SECRET_KEY, algorithm=JWT_ALGO)


@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register_player(db: db_dependency, player_body: PlayerValidation = Body()):
    #return {"message": "Player registered successfully", "player": player_body}
    new_player = Players(
        email=player_body.email,
        username=player_body.username,
        first_name=player_body.first_name,
        last_name=player_body.last_name,
        hashed_password=bcrypt_context.hash(player_body.password),  # In a real application, hash the password before storing
        role=player_body.role
    )
    db.add(new_player)
    db.commit()
   # db.refresh(new_player)
   #return new_player


@router.post("/auth/login")
async def login_player(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency,):
    player_authenticated = authenticate_player(db, form_data.username, form_data.password)
    #player = authenticate_player(db, form_data.username, form_data.password)
    if player_authenticated is None:
        return {"error": "Invalid username or password"}
    else:
        token = create_token(player_authenticated.username, player_authenticated.id, timedelta(minutes=30))
        return token 
        #{"message": "Login successful", "player": player_authenticated, "token": token}

