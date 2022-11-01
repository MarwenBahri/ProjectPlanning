from pydantic import BaseModel, EmailStr

class PassReset(BaseModel):
    password: str
    code: str