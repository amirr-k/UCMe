from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserResponse, UserProfileUpdate, UserPreferencesUpdate
from utils.jwt_auth import getCurrentUser

#All routes start with /profile
router = APIRouter(tags=["Profile"], prefix="/profile")

#Get current user's profile
@router.get("/me", response_model=UserResponse)
def getUserProfile(current_user: User = Depends(getCurrentUser)):
    return current_user

@router.get("/{userID}", response_model=UserResponse)
def getUserProfile(userID: int, db: Session = Depends(get_db), currentUser: User = Depends(getCurrentUser)):
    user = db.query(User).filter(User.id == userID).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return user

@router.put("/update", response_model=UserResponse)
def updateProfile(profileData: UserProfileUpdate, db: Session = Depends(get_db), currentUser: User = Depends(getCurrentUser)):
    for key, value in profileData.dict(exclude_unset=True).items():
        setattr(currentUser, key, value)
    
    db.commit()
    db.refresh(currentUser)
    return currentUser

@router.put("/preferences", response_model=UserResponse)
def update_preferences(
    preferences_data: UserPreferencesUpdate,  # Use your preferences schema
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update the current user's matchmaking preferences"""
    # Update user preferences from the request data
    for key, value in preferences_data.dict(exclude_unset=True).items():
        setattr(curren