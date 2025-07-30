from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SwipeCreate(BaseModel):
    targetId: int
    isLike: bool

class SwipeResponse(BaseModel):
    id: int
    targetId: int
    isLike: bool
    isMatch: bool
    matchId: Optional[int] = None
    
    class Config:
        from_attributes = True