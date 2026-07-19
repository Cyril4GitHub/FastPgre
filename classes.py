from typing import List, Optional
from pydantic import BaseModel, Field, constr


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