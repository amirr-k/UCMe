from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from models.images import Image
from models.user import User
from schemas.images import ImageCreate, ImageResponse, ImageUpdate
from utils.jwt_auth import getCurrentUser
from sqlalchemy.exc import IntegrityError
import os
import uuid
from typing import List
import shutil

router = APIRouter(tags=["Images"])

# Configuration for image storage
UPLOAD_DIR = "uploads/images"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic", ".heif", ".jfif"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

def is_valid_image_file(filename: str) -> bool:
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)

def save_image_file(file: UploadFile, user_id: int) -> str:

    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1].lower()
    unique_filename = f"{user_id}_{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return file_path

@router.post("/upload", response_model=ImageResponse)
async def uploadImage(
    file: UploadFile = File(...),
    isPrimary: bool = Form(False),
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):
    
    # Validate file type
    if not is_valid_image_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Enforce maximum of 3 images per user
    current_count = db.query(Image).filter(Image.userId == currentUser.id).count()
    if current_count >= 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum of 3 images allowed"
        )
    
    # Check file size safely
    try:
        current_pos = file.file.tell()
    except Exception:
        current_pos = 0
    try:
        file.file.seek(0, os.SEEK_END)
        size_bytes = file.file.tell()
    finally:
        file.file.seek(current_pos, os.SEEK_SET)
    if size_bytes and size_bytes > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    try:
        # Save the file (ensure pointer at start)
        file.file.seek(0)
        file_path = save_image_file(file, currentUser.id)
        
        # If this is set as primary, unset other primary images
        if isPrimary:
            db.query(Image).filter(
                Image.userId == currentUser.id,
                Image.isPrimary == True
            ).update({"isPrimary": False})
        
        # Create image record
        image = Image(
            userId=currentUser.id,
            imageUrl=file_path,
            isPrimary=isPrimary
        )
        
        db.add(image)
        db.commit()
        db.refresh(image)
        
        return image
        
    except Exception as e:
        db.rollback()
        # Clean up uploaded file if database operation fails
        if 'file_path' in locals():
            try:
                os.remove(file_path)
            except:
                pass
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload image"
        )

@router.get("/my-images", response_model=List[ImageResponse])
async def getMyImages(
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):
    images = db.query(Image).filter(Image.userId == currentUser.id).all()
    return images

@router.put("/{imageId}/set-primary", response_model=ImageResponse)
async def setPrimaryImage(
    imageId: int,
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):
    
    # Get the image
    image = db.query(Image).filter(
        Image.id == imageId,
        Image.userId == currentUser.id
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    try:
        # Unset all other primary images for this user
        db.query(Image).filter(
            Image.userId == currentUser.id,
            Image.isPrimary == True
        ).update({"isPrimary": False})
        
        # Set this image as primary
        image.isPrimary = True
        db.commit()
        db.refresh(image)
        
        return image
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to set primary image"
        )

@router.delete("/{imageId}")
async def deleteImage(
    imageId: int,
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):
    
    # Get the image
    image = db.query(Image).filter(
        Image.id == imageId,
        Image.userId == currentUser.id
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    # Don't allow deletion of the only image if it's primary
    user_image_count = db.query(Image).filter(Image.userId == currentUser.id).count()
    if user_image_count == 1 and image.isPrimary:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete the only image. Please upload another image first."
        )
    
    try:
        # Delete the file from storage
        if os.path.exists(image.imageUrl):
            os.remove(image.imageUrl)
        
        # Delete from database
        db.delete(image)
        db.commit()
        
        return {"message": "Image deleted successfully"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete image"
        )

@router.put("/{imageId}", response_model=ImageResponse)
async def updateImage(
    imageId: int,
    imageUpdate: ImageUpdate,
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):
    
    # Get the image
    image = db.query(Image).filter(
        Image.id == imageId,
        Image.userId == currentUser.id
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    try:
        update_data = imageUpdate.dict(exclude_none=True)
        
        # Handle primary image logic
        if 'isPrimary' in update_data and update_data['isPrimary']:
            # Unset other primary images
            db.query(Image).filter(
                Image.userId == currentUser.id,
                Image.id != imageId,
                Image.isPrimary == True
            ).update({"isPrimary": False})
        
        # Update the image
        for field, value in update_data.items():
            if hasattr(image, field):
                setattr(image, field, value)
        
        db.commit()
        db.refresh(image)
        
        return image
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update image"
        ) 