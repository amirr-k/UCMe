from sqlalchemy import ARRAY, Column, Integer, String, Boolean, ForeignKey, DateTime, Text
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
    createdAt = Column(DateTime, server_default=func.now()) #Self explanatory, set to current time

    #Profile Information
    bio = Column(Text, nullable=True) #Self explanatory
    interests = Column(ARRAY(String), nullable=True) #Self explanatory
    classes = Column(ARRAY(String), nullable=True) #May remove this i'm not sure 
    profilePic = Column(String, nullable=True) #URL of Profile Picture
    lookingFor = Column(String, nullable=True) #Friend, Dating, Relationship, etc
    smokes = Column(Boolean, default=False) #True, False
    drinks = Column(Boolean, default=False) #True, False 
    pronouns = Column(String, nullable=True) #He/Him, She/Her, They/Them, etc
    location = Column(String, nullable=True) #Location (City, State)
    hometown = Column(String, nullable=True) #Hometown (City, State)
    lastSeen = Column(DateTime, nullable=True) #Last Time User Was Seen Online


    
    #Matchmaking Preferences
    minAge = Column(Integer, nullable=True) #Minimum Age
    maxAge = Column(Integer, nullable=True) #Maximum Age
    genderPref= Column(String, nullable=True) #Male, Female, Other (Specified)
    otherColleges = Column(ARRAY(String), nullable=True) #Other Colleges (Specified)
    majors = Column(ARRAY(String), nullable=True) #Majors (Specified)
    

    
    
    


    
    

    