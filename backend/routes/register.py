from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserCreate, UserResponse, EmailVerificationRequest, EmailVerificationResponse
from datetime import datetime
from utils.auth import generate_verification_code, store_verification_code, get_verification_code, delete_verification_code, send_verification_email
from sqlalchemy.exc import IntegrityError

router = APIRouter()

validEmails = {"@ucsd.edu", "@ucdavis.edu", "@ucr.edu", "@ucla.edu", "@uci.edu"
               ,"ucsc.edu", "@ucmerced.edu", "@ucsb.edu", "@berkeley.edu"}


@router.post("/send-verification")
def send_email_code(email: str, db: Session = Depends(get_db)):
    if not any(email.endswith(domain) for domain in validEmails):
        raise HTTPException(400, "Please enter your University of California Email Address")
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(409, "Email already registered! Proceed to login.")
    
    code = generate_verification_code()
    store_verification_code(email, code)
    send_verification_email(email, code)
    return EmailVerificationResponse(message="Verification email sent", verified=False)

@router.post("/verify-email", response_model=EmailVerificationResponse)
def verify_email(payload: EmailVerificationRequest, db: Session = Depends(get_db)):
    code = get_verification_code(payload.email)
    if not code or code != payload.verification_code:
        raise HTTPException(400, "Invalid verification code")
    delete_verification_code(payload.email)
    return EmailVerificationResponse(message="Email verified", verified=True)

@router.post("/resend-email", response_model=EmailVerificationResponse)
def resend_verification_email(payload: EmailVerificationRequest, db: Session = Depends(get_db)):
    if not any(payload.email.endswith(domain) for domain in validEmails):
        raise HTTPException(400, "Please enter your University of California Email Address")
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(409, "Email already registered! Proceed to login.")
    code = generate_verification_code()
    store_verification_code(payload.email, code)
    send_verification_email(payload.email, code)
    return EmailVerificationResponse(message="Verification email sent", verified=False)

@router.post("/register", response_model=UserResponse)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
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
    try:
        db.add(insertUser)
        db.commit()
        db.refresh(insertUser)
        return insertUser
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Could not create user. Please try again.")

