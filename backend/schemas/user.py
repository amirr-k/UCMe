# schemas/user.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime

#Base user schema with common fields
class UserBase(BaseModel):
    email: EmailStr

#For creating a new user (registration)
class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=2, max_length=100)
    college: str #This is a restricted field, so we don't need to validate it
    school: str #Same with this
    year: int #Same with this
    gender: str = Field(min_length=2, max_length=100) #Allows for self defined gender
    major: str = Field(min_length=2, max_length=100) #Allows for self defined major
    verification_code: str #Verification Code for Account Creation

    bio: str = Field(min_length=10, max_length=500)
    interests: List[str] = Field(min_items=1) #At least one interest required
    classes: List[str] = [] #Optional but initialized as empty list
    lookingFor: str #Restricted field, so we don't need to validate it
    smokes: bool = False #Defaulted
    drinks: bool = False #Defaulted
    pronouns: str = Field(min_length=1) #Allows for self defined pronouns
    location: str = Field(min_length=1) #Allows for self defined location
    hometown: str = Field(min_length=1) #Allows for self defined hometown

    minAge: int = Field(ge=18, le=100)  #Minimum Age
    maxAge: int = Field(ge=18, le=100) #Maximum Age
    genderPref: str = Field(min_length=1) #Gender Preference
    otherColleges: List[str] = []  #Other Colleges (Specified)
    majors: List[str] = []  #Majors (Specified)

    #Validator for maxAge and minAge
    @validator('maxAge')
    def maxAge_must_be_greater_than_minAge(cls, v, values):
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

#For images
class ImageResponse(BaseModel):
    id: int
    image_url: str
    is_primary: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

#Complete user response
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    college: str
    school: str
    year: int
    gender: str
    major: str
    created_at: datetime
    bio: str
    interests: List[str]
    classes: List[str]
    lookingFor: str
    smokes: bool
    drinks: bool
    pronouns: str
    location: str
    hometown: str
    minAge: int
    maxAge: int
    genderPref: str
    otherColleges: List[str]
    majors: List[str]
    images: List[ImageResponse] = []
    
    class Config:
        from_attributes = True

#For auth. endpoints
class EmailVerificationRequest(BaseModel):
    email: EmailStr
    verification_code: str

class EmailVerificationResponse(BaseModel):
    message: str
    verified: bool