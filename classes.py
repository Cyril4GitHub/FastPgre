from dataclasses import field
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, constr, field_validator


class Hero:
    id: int
    nick_name: str
    full_name: str
    occupation: List[str]
    powers: List[str]
    hobby: List[str]
    type: str
    rank: int
    def __init__(self, id, nick_name, full_name, occupation, powers, hobby, type, rank):
        self.id = id
        self.nick_name = nick_name
        self.full_name = full_name
        self.occupation = occupation
        self.powers = powers
        self.hobby = hobby
        self.type = type
        self.rank = rank

class HeroValidation(BaseModel):
    id: Optional[int] = Field(default=None, ge=0, description="ID is not mandatory on creation") # int
    nick_name: str = Field(min_length=3)
    full_name: str = Field(min_length=3)
    occupation: List[constr(min_length=3)]  # type: ignore     #List[str]
    powers: List[constr(min_length=3)] # type: ignore    #List[str]
    hobby: List[constr(min_length=3)] # type: ignore    #List[str]
    type: constr(min_length=3) # type: ignore    #List[str]
    rank: int = Field(ge=0, le=100) # gt or lt
    model_config = {
        "json_schema_extra": {
            "example": {
                "nick_name": "Superman",
                "full_name": "Clark Kent",
                "occupation": ["Journalist", "Hero"],
                "powers": ["Flight", "Super Strength", "X-ray Vision"],
                "hobby": ["Reading", "Photography"],
                "type": ["Alien", "Hero"],
                "rank": 95
            }
        }
    }


AllowedRoles = Literal[ "admin", "moderator", "player"]

class PlayerValidation(BaseModel):
    email: str = Field(min_length=5)
    username: str = Field(min_length=3)
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    password: str = Field(min_length=8)
    role: AllowedRoles = Field(description="The role of the player")
    # PRE VALIDATOR
    @field_validator("role", mode="before")
    @classmethod
    def lower_case_role(cls, val: str) -> str:
        return val.lower()
    
    # def validate_role(cls, v):
    #     if v not in AllowedRoles.__args__:
    #         raise ValueError(f"Invalid role. Must be one of {AllowedRoles.__args__}")
    #     return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "player1@example.com",
                "username": "player1",
                "first_name": "John",
                "last_name": "Doe",
                "password": "securepassword",
                "role": "player"
            }
        }
    }