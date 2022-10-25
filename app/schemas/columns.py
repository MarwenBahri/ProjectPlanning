from pydantic import BaseModel
from datetime import datetime


class Column(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    project_id: int

    class Config:
        orm_mode = True