from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ColumnBase(BaseModel):
    name: str
    description: Optional[str]
    project_id: int
    

class ColumnCreate(ColumnBase):
    pass

class ColumnOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    project_id: int

    class Config:
        orm_mode = True