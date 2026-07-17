from typing import List

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