from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from .user import UserResponse

class MessageBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    conversationId: int
    senderId: int
    isRead: bool
    createdAt: datetime
    
    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    pass

class ConversationCreate(ConversationBase):
    userId2: int 

class ConversationSummary(BaseModel):
    id: int
    userId1: int
    userId2: int
    lastMessageAt: datetime
    createdAt: datetime
    lastMessage: Optional[MessageResponse] = None
    otherUser: UserResponse
    unreadCount: int
    
    class Config:
        from_attributes = True

class ConversationDetail(ConversationSummary):
    messages: List[MessageResponse]
    
    class Config:
        from_attributes = True