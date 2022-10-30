from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

class TeamBase(BaseModel):
    name : str
    description : Optional[str]
    is_personal : bool

class TeamOut(TeamBase):
    id : int
    created_at : datetime
    owner_id : int
    class Config : 
        orm_mode = True

class TeamsOut(BaseModel):
    teams : List[TeamOut]
    class Config : 
        orm_mode = True
