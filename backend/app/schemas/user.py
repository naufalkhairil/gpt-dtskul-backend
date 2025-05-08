from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.user import UserRole

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.USER

class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None

class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole
    created_at: datetime

class User(UserBase):
    id: int
    role: UserRole
    is_active: bool

    class Config:
        orm_mode = True

class UserToken(BaseModel):
    access_token: str
    token_type: str
