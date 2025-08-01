from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserResponse, UserProfileUpdate, UserPreferencesUpdate
from utils.jwt_auth import getCurrentUser
from sqlalchemy.exc import IntegrityError

router = APIRouter(tags=["Profile"])

@router.get("/me", response_model=UserResponse)
async def getCurrentUserProfile(
    currentUser: User = Depends(getCurrentUser)
):
    return currentUser

@router.put("/update", response_model=UserResponse)
async def updateProfile(
    profileData: UserProfileUpdate,
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):
    
    # Get current user from database to ensure fresh data
    user = db.query(User).filter(User.id == currentUser.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update only provided fields (exclude_none in schema handles this)
    updateData = profileData.dict(exclude_none=True)
    
    for field, value in updateData.items():
        if hasattr(user, field):
            setattr(user, field, value)
    
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        db.rollback()
        print(f"Profile update error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update profile"
        )

@router.put("/preferences", response_model=UserResponse)
async def updatePreferences(
    preferencesData: UserPreferencesUpdate,
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):
    
    # Get current user from database
    user = db.query(User).filter(User.id == currentUser.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update preference fields
    updateData = preferencesData.dict(exclude_none=True)
    
    for field, value in updateData.items():
        if hasattr(user, field):
            setattr(user, field, value)
    
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        db.rollback()
        print(f"Preferences update error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update preferences"
        )

@router.get("/viewProfile/{userId}", response_model=UserResponse)
async def viewOtherUserProfile(
    userId: int,
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):
    
    # Find the user profile
    user = db.query(User).filter(
        User.id == userId,
        User.moderationStatus == "Approved"
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    if user.id == currentUser.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use /me endpoint to view your own profile"
        )
    
    return user

@router.delete("/delete")
async def deleteProfile(
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):
    
    # Get current user from database
    user = db.query(User).filter(User.id == currentUser.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    try:
        # SQLAlchemy cascade deletions will handle related records (images, swipes, matches)
        db.delete(user)
        db.commit()
        
        return {"message": "Profile deleted successfully"}
    except Exception as e:
        db.rollback()
        print(f"Profile deletion error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete profile"
        )