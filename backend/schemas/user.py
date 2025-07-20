from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str
    name: str
    college: str
    school: str
    year: int
    gender: str
    major: str
    profile_pic_url: Optional[str] = None
    bio: Optional[str] = None
    interests: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: Optional[datetime]
    class Config:
        orm_mode = True