from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserResponse
from datetime import datetime
from utils.auth import generate_verification_code, store_verification_code, get_verification_code, delete_verification_code, send_verification_email

router = APIRouter()

@router.post("/login")
def login_code(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found. Please register first."
        )
    code = generate_verification_code()
    store_verification_code(email, code)
    send_verification_email(email, code)
    return {"message": "Verification code sent to email"}

@router.post("/login")
def login_user(email: str, verification_code: str, db: Session = Depends(get_db)):
    stored_code = get_verification_code(email)
    if not stored_code or stored_code != verification_code:
        raise HTTPException(status_code=400,detail="Invalid verification code!")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found!")
    delete_verification_code(email)
    return {"message": "Login successful", "user": user}
