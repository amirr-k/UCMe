from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import base

class Image(base):
    __tablename__ = 'images'
    
    id = Column(Integer, primary_key=True, index=True)
    userID = Column(Integer, ForeignKey('users.id'), nullable=False)
    imageURL = Column(String, nullable=False)
    createdAt = Column(DateTime, server_default=func.now())
    
    # Relationship to User model
    user = relationship("User", back_populates="images")