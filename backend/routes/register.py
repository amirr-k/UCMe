from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserCreate, UserResponse
from datetime import datetime


router = APIRouter()

validEmails = {"@ucsd.edu", "@ucdavis.edu", "@ucr.edu", "@ucla.edu", "@uci.edu"
               ,"ucsc.edu", "@ucmerced.edu", "@ucsb.edu", "@berkeley.edu"}

@router.post("/signup", response_model=UserResponse)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    if not any(payload.email.endswith(domain) for domain in validEmails):
        raise HTTPException(400, "Please enter your University of California Email Address")
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(409, "Email already registered! Proceed to login.")
    
    insertUser= User(
        email=payload.email,
        name=payload.name,
        college=payload.college,
        school=payload.school,
        year=payload.year,
        gender=payload.gender,
        major=payload.major,
        created_at=datetime.utcnow(),
    )
    db.add(insertUser)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Could not create user. Please try again.")
    
    db.commit()
    db.refresh(insertUser)
    return insertUser
  
@router.post("/login", response_model=UserResponse, status_code=201)

