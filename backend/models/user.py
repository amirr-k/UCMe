from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from database import base

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
    created_at = Column(DateTime) 
    profile_pic_url = Column(String, nullable=True)  
    bio = Column(Text, nullable=True)
    

    