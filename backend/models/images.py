from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import base

class Image(base):
    __tablename__ = 'images'
    
    # Primary key and identification
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey('users.id'), nullable=False)
    imageUrl = Column(String, nullable=False) # URL/path to the image file
    isPrimary = Column(Boolean, default=False, nullable=False) # Whether this is the user's main profile picture
    createdAt = Column(DateTime, server_default=func.now())
    
    user = relationship("User", backref="images")

   