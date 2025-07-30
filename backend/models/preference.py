from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import base

class PreferenceStrength(base):
    __tablename__ = 'preference_strengths'
    
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey('users.id'), nullable=False)
    category = Column(String, nullable=False)  # "location", "age", "interests", etc.
    strength = Column(Float, nullable=False, default=1.0)  # 0.0 to 1.0
    
    user = relationship("User", backref="preferenceStrengths")