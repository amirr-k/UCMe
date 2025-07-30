from pydantic import BaseModel
from datetime import datetime
from .user import UserResponse

class MatchUserResponse(BaseModel):
    matchId: int
    createdAt: datetime
    user: UserResponse
    
    class Config:
        from_attributes = True

class MatchResponse(BaseModel):
    id: int
    createdAt: datetime
    user: UserResponse
    
    class Config:
        from_attributes = True