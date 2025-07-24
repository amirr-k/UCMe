from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserResponse
from utils.jwt_auth import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/profile/{user_id}", response_model=UserResponse)
def get_user_profile(user_id: int, current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, detail="User not found!")
    return user

@router.put("/me", response_model=UserResponse)
def update_profile(
    name: str = None,
    college: str = None,
    school: str = None,
    year: str = None,
    gender: str = None,
    major: str = None,
    profile_pic_url: str = None,
    bio: str = None,
    interests: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    if bio is not None:
        current_user.bio = bio
    if interests is not None:
        current_user.interests = interests
    if name is not None:
        current_user.name = name
    if college is not None:
        current_user.college = college
    if year is not None:
        current_user.year = year
    if gender is not None:
        current_user.gender = gender
    if major is not None:
        current_user.major = major
    if profile_pic_url is not None:
        current_user.profile_pic_url = profile_pic_url
    db.commit()
    db.refresh(current_user)
    return current_user