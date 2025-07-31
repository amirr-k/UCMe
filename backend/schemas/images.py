from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from models.images import Image

# Base image schema
class ImageBase(BaseModel):
    imageUrl: str

# For creating a new image
class ImageCreate(ImageBase):
    isPrimary: bool = False

# For updating an image
class ImageUpdate(BaseModel):
    imageUrl: Optional[str] = None
    isPrimary: Optional[bool] = None
    
    class Config:
        exclude_none = True

# Complete image response schema
class ImageResponse(ImageBase):
    id: int
    userId: int
    imageUrl: str # URL/path to the image file
    isPrimary: bool # Whether this is the user's main profile picture
    createdAt: datetime # When image was uploaded
    
    class Config:
        from_attributes = True