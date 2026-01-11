from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "officer"  # admin or officer

class UserResponse(UserBase):
    id: int
    is_active: bool
    role: str
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True
