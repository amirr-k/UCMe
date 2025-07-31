from sqlalchemy import ARRAY, Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from database import base
from sqlalchemy.sql import func

class User(base):
    __tablename__ = 'users'
    
    # Basic User Information
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False) # University email address
    name = Column(String, nullable=False) # First and last name
    college = Column(String, nullable=False) # UC campus (UCLA, Berkeley, etc)
    school = Column(String, nullable=False) # Specific school within campus (Engineering, L&S, etc)
    year = Column(Integer, nullable=False) # Graduation year (2024, 2025, etc)
    age = Column(Integer, nullable=False) # Current age of user
    gender = Column(String, nullable=False) # Self-defined gender identity
    major = Column(String, nullable=False) # Academic major
    moderationStatus = Column(String, nullable=False, default="Pending") # Account status: Pending, Approved, Rejected
    createdAt = Column(DateTime, server_default=func.now()) # Account creation timestamp

    # Profile Information
    bio = Column(Text, nullable=False) # Personal description/bio
    interests = Column(ARRAY(String), nullable=False) # List of user interests and hobbies
    classes = Column(ARRAY(String), nullable=False) # Current classes (for finding study partners)
    lookingFor = Column(String, nullable=False) # What user is seeking (Dating, Friends, Relationship, etc)
    smokes = Column(Boolean, default=False) # Smoking preference
    drinks = Column(Boolean, default=False) # Drinking preference
    pronouns = Column(String, nullable=False) # Preferred pronouns (He/Him, She/Her, They/Them, etc)
    location = Column(String, nullable=False) # Current location (City, State)
    hometown = Column(String, nullable=False) # User's hometown (City, State)

    # Matchmaking Preferences - what user is looking for in matches
    minAge = Column(Integer, nullable=False) # Minimum preferred age for matches
    maxAge = Column(Integer, nullable=False) # Maximum preferred age for matches
    genderPref = Column(String, nullable=False) # Preferred gender for matches
    otherColleges = Column(ARRAY(String), nullable=False) # Other UC campuses user wants to see
    majors = Column(ARRAY(String), nullable=False) # Preferred majors for matches

    # Relationships to other models
    images = relationship("Image", back_populates="user", cascade="all, delete-orphan") # User's profile images

    #Interaction and Match Relationships
    sentSwipes = relationship("Swipe", foreign_keys="Swipe.userId", backref="sender") # Likes sent by this user
    receivedSwipes = relationship("Swipe", foreign_keys="Swipe.targetId", backref="target") # Likes received by this user
    matchesAsUser1 = relationship("Match", foreign_keys="Match.userId1", backref="user1") # Matches where this user is user1
    matchesAsUser2 = relationship("Match", foreign_keys="Match.userId2", backref="user2") # Matches where this user is user2
    

    
    

    