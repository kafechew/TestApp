# schemas.py

from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    id: int

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    author_id: int

class Post(PostBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True