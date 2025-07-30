from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from models.images import Image

#Base image schema
class ImageBase(BaseModel):
    image_url: str
    is_primary: bool = False

#For creating a new image
class ImageCreate(ImageBase):
    pass

#For updating an image
class ImageUpdate(BaseModel):
    is_primary: Optional[bool] = None
    
    class Config:
        exclude_none = True

class ImageResponse(ImageBase):
    id: int
    user_id: int
    createdAt: datetime
    
    class Config:
        from_attributes = True