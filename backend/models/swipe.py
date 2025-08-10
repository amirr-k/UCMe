from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime, Index
from sqlalchemy.sql import func
from database import base

class Swipe(base):
    __tablename__ = 'swipes'
    
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey('users.id'), nullable=False)
    targetId = Column(Integer, ForeignKey('users.id'), nullable=False)
    isLike = Column(Boolean, nullable=False)
    createdAt = Column(DateTime, server_default=func.now())

    __table_args__ = (Index('idx_swipe_user_target', userId, targetId, unique=True),)