from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr



class UserBase(BaseModel):
    name : str
    lastname : str
    email : EmailStr
    password : str
    phone_number: Optional[str]
    
    class Config : 
        use_enum_values = True

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id : int
    created_at : datetime
    class Config : 
        orm_mode = True


