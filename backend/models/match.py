from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from database import base

class Match(base):
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True, index=True)
    userId1 = Column(Integer, ForeignKey('users.id'), nullable=False)
    userId2 = Column(Integer, ForeignKey('users.id'), nullable=False)
    createdAt = Column(DateTime, server_default=func.now())