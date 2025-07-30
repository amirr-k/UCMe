from sqlalchemy import ARRAY, Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from database import base
from sqlalchemy.sql import func

class User(base):
    __tablename__ = 'users'
    
    #Basic User Information
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False) #First and Last Name, Self Def.
    college = Column(String, nullable=False) #Which UC Campus (Restricted)
    school = Column(String, nullable=False) #For UCSD, College System, for others, L&S, Engineering, etc
    year = Column(Integer, nullable=False) #'2025, '2026, etc
    gender = Column(String, nullable=False)# Male, Female, Other (Specified)
    major = Column(String, nullable=False) #Major -- Self Def.
    createdAt = Column(DateTime, server_default=func.now()) #Self explanatory, set to current time

    #Profile Information
    bio = Column(Text, nullable=False) #Self explanatory
    interests = Column(ARRAY(String), nullable=False) #Self explanatory
    classes = Column(ARRAY(String), nullable=False) #May remove this i'm not sure 
    lookingFor = Column(String, nullable=False) #Friend, Dating, Relationship, etc
    smokes = Column(Boolean, default=False) #True, False
    drinks = Column(Boolean, default=False) #True, False 
    pronouns = Column(String, nullable=False) #He/Him, She/Her, They/Them, etc
    location = Column(String, nullable=False) #Location (City, State)
    hometown = Column(String, nullable=False) #Hometown (City, State)

    
    #Matchmaking Preferences
    minYear = Column(Integer, nullable=False) #Minimum Year
    maxYear = Column(Integer, nullable=False) #Maximum Year
    genderPref= Column(String, nullable=False) #Male, Female, Other (Specified)
    otherColleges = Column(ARRAY(String), nullable=False) #Other Colleges (Specified)
    majors = Column(ARRAY(String), nullable=False) #Majors (Specified)

    images = relationship("Image", back_populates="user", cascade="all, delete-orphan")

    #Swipe and Match Relationships
    sent_swipes = relationship("Swipe", foreign_keys="Swipe.userId", backref="sender")
    received_swipes = relationship("Swipe", foreign_keys="Swipe.targetId", backref="target")
    matches_as_user1 = relationship("Match", foreign_keys="Match.userId1", backref="user1")
    matches_as_user2 = relationship("Match", foreign_keys="Match.userId2", backref="user2")
    

    
    
    


    
    

    