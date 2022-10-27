from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

class TeamBase(BaseModel):
    name : str
    description : Optional[str]
    owner_id : int
    is_personal : bool

class TeamOut(TeamBase):
    id : int
    created_at : datetime
    class Config : 
        orm_mode = True

class TeamsOut(BaseModel):
    teams : List[TeamOut]
    class Config : 
        orm_mode = True
