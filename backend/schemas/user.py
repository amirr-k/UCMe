from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime

# Base user schema with common fields
class UserBase(BaseModel):
    email: EmailStr

# For creating a new user (registration)
class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=2, max_length=100)
    college: str # UC campus (restricted list)
    school: str # Specific school within campus
    year: int # Graduation year (2024, 2025, etc)
    age: int = Field(ge=18, le=100) # Current age of user
    gender: str = Field(min_length=2, max_length=100) # Self-defined gender
    major: str = Field(min_length=2, max_length=100) # Academic major
    verificationCode: str # Email verification code for account creation

    bio: str = Field(min_length=10, max_length=500) # Personal bio/description
    interests: List[str] = Field(min_items=1) # List of interests (at least one required)
    classes: List[str] = [] # Current classes (optional)
    lookingFor: str # What user is seeking (dating, friends, etc)
    smokes: bool = False # Smoking preference
    drinks: bool = False # Drinking preference  
    pronouns: str = Field(min_length=1) # Preferred pronouns
    location: str = Field(min_length=1) # Current location
    hometown: str = Field(min_length=1) # Hometown

    minAge: int = Field(ge=18, le=100) # Minimum preferred age for matches
    maxAge: int = Field(ge=18, le=100) # Maximum preferred age for matches
    genderPref: str = Field(min_length=1) # Preferred gender for matches
    otherColleges: List[str] = [] # Other UC campuses user wants to see
    majors: List[str] = [] # Preferred majors for matches

    # Validator to ensure maxAge is greater than or equal to minAge
    @validator('maxAge')
    def validateAgeRange(cls, v, values):
        if 'minAge' in values and v < values['minAge']:
            raise ValueError('maxAge must be greater than or equal to minAge')
        return v



#Necessary for updating user profile
class UserProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)  #If provided, can't be empty
    college: Optional[str] = Field(None, min_length=1)
    school: Optional[str] = Field(None, min_length=1)
    year: Optional[int] = Field(None, ge=2000, le=2030)
    gender: Optional[str] = Field(None, min_length=1)
    major: Optional[str] = Field(None, min_length=1)
    bio: Optional[str] = Field(None, min_length=10, max_length=500)
    interests: Optional[List[str]] = Field(None, min_items=1)
    classes: Optional[List[str]] = None
    lookingFor: Optional[str] = Field(None, min_length=1)
    smokes: Optional[bool] = None
    drinks: Optional[bool] = None
    pronouns: Optional[str] = Field(None, min_length=1)
    location: Optional[str] = Field(None, min_length=1)
    hometown: Optional[str] = Field(None, min_length=1)

    class Config:
        #Ensures that None values are excluded when converting to dict
        exclude_none = True

#For updating preferences
class UserPreferencesUpdate(BaseModel):
    minAge: Optional[int] = Field(None, ge=18, le=100)
    maxAge: Optional[int] = Field(None, ge=18, le=100)
    genderPref: Optional[str] = Field(None, min_length=1)
    otherColleges: Optional[List[str]] = None
    majors: Optional[List[str]] = None
    
    @validator('maxAge')
    def maxAge_must_be_greater_than_minAge(cls, v, values):
        if v is not None and 'minAge' in values and values['minAge'] is not None:
            if v < values['minAge']:
                raise ValueError('maxAge must be greater than or equal to minAge')
        return v
    
    class Config:
        #Ensures that None values are excluded when converting to dict
        exclude_none = True

# Schema for user profile images
class ImageResponse(BaseModel):
    id: int
    imageUrl: str # URL/path to the image file
    isPrimary: bool # Whether this is the user's main profile picture
    createdAt: datetime # When image was uploaded
    
    class Config:
        from_attributes = True

# Complete user profile response 
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    college: str
    school: str
    year: int # Graduation year
    age: int # Current age
    gender: str
    major: str
    createdAt: datetime # Account creation timestamp
    bio: str
    interests: List[str]
    classes: List[str]
    lookingFor: str
    smokes: bool
    drinks: bool
    pronouns: str
    location: str
    hometown: str
    minAge: int # Minimum preferred age for matches
    maxAge: int # Maximum preferred age for matches
    genderPref: str # Preferred gender for matches
    otherColleges: List[str] # Other UC campuses user wants to see
    majors: List[str] # Preferred majors for matches
    images: List[ImageResponse] = [] # User's profile images
    
    class Config:
        from_attributes = True

# Schema for email verification requests (login and registration)
class EmailVerificationRequest(BaseModel):
    email: EmailStr
    verificationCode: str # 6-digit verification code sent to email

# Schema for email verification responses
class EmailVerificationResponse(BaseModel):
    message: str # Status message for user
    verified: bool # Whether verification was successful

# Schema for JWT authentication tokens
class Token(BaseModel):
    accessToken: str # JWT token for authenticated requests
    tokenType: str # Token type (always "bearer")