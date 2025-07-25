from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str
    college: str
    school: str
    year: int
    gender: str
    major: str
    profile_pic_url: Optional[str] = None
    bio: Optional[str] = None

class UserCreate(UserBase):
    verification_code: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class EmailVerificationRequest(BaseModel):
    email: EmailStr
    verification_code: str

class EmailVerificationResponse(BaseModel):
    message: str
    verified: bool