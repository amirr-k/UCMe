from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserCreate, UserResponse
from datetime import datetime


router = APIRouter()

validEmails = {"@ucsd.edu", "@ucdavis.edu", "@ucr.edu", "@ucla.edu", "@uci.edu"
               ,"ucsc.edu", "@ucmerced.edu", "@ucsb.edu", "@berkeley.edu"}

@router.post("/signup", response_model=UserResponse)

#May need to change this to UserCreate...
def create_user(user: UserBase, db: Session = Depends(get_db)):
    new_user = ()
    #Figure out how to verify email before creating the user.