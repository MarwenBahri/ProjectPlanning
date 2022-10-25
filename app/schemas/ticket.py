from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel
from .ticket_priority import TicketPriority


class TicketBase(BaseModel):
    name : str
    description : Optional[str]
    deadline : Optional[datetime]
    priority : TicketPriority
    column_id : int
    class Config : 
        use_enum_values = True

class TicketOut(TicketBase):
    id : int
    created_at : datetime
    class Config : 
        orm_mode = True

class TicketsOut(BaseModel):
    tickets : List[TicketOut]
    class Config : 
        orm_mode = True
