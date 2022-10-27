from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class ProjectBase(BaseModel):
    name : str
    description : Optional[str]
    team_id : int

class ProjectOut(ProjectBase):
    id : int
    created_at : datetime
    class Config : 
        orm_mode = True

class ProjectsOut(BaseModel):
    projects : List[ProjectOut]
    class Config : 
        orm_mode = True

