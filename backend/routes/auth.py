from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserCreate, UserResponse, EmailVerificationRequest, EmailVerificationResponse, Token
from utils.auth import generate_verification_code, store_verification_code, get_verification_code, delete_verification_code, send_verification_email
from utils.jwt_auth import create_access_token
from sqlalchemy.exc import IntegrityError
from datetime import datetime

router = APIRouter(tags=["Authentication"])

#Valid UC email domains
validEmails = {
    "@ucsd.edu", "@ucdavis.edu", "@ucr.edu", "@ucla.edu", "@uci.edu",
    "@ucsc.edu", "@ucmerced.edu", "@ucsb.edu", "@berkeley.edu"
}

#Registration endpoints
@router.post("/register/send-verification", response_model=EmailVerificationResponse)
async def send_register_verification(email: str, db: Session = Depends(get_db)):
    #Validate UC email
    if not any(email.endswith(domain) for domain in validEmails):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Please enter your University of California Email Address"
        )
    
    #Check if email is already registered
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Email already registered! Please login instead."
        )
    
    #Generate and store verification code
    code = generate_verification_code()
    success = store_verification_code(email, code)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to store verification code. Please try again."
        )
    
    #Send verification email
    sent = send_verification_email(email, code)
    if not sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to send verification email. Please try again."
        )
    
    return EmailVerificationResponse(message="Verification email sent", verified=False)

@router.post("/register/resend", response_model=EmailVerificationResponse)
async def resend_verification_email(payload: EmailVerificationRequest, db: Session = Depends(get_db)):
    # Validate UC email
    if not any(payload.email.endswith(domain) for domain in validEmails):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Please enter your University of California Email Address"
        )
    
    # Check if email is already registered
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Email already registered! Please login instead."
        )
    
    # Generate and store new verification code
    code = generate_verification_code()
    store_verification_code(payload.email, code)
    send_verification_email(payload.email, code)
    
    return EmailVerificationResponse(message="Verification email resent", verified=False)

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Verify the verification code
    stored_code = get_verification_code(user_data.email)
    if not stored_code or stored_code != user_data.verification_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid or expired verification code"
        )
    
    # Create new user
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        college=user_data.college,
        school=user_data.school,
        year=user_data.year,
        gender=user_data.gender,
        major=user_data.major,
        bio=user_data.bio,
        interests=user_data.interests,
        classes=user_data.classes,
        lookingFor=user_data.lookingFor,
        smokes=user_data.smokes,
        drinks=user_data.drinks,
        pronouns=user_data.pronouns,
        location=user_data.location,
        hometown=user_data.hometown,
        minYear=user_data.minAge,  # Adjust field name if necessary
        maxYear=user_data.maxAge,  # Adjust field name if necessary
        genderPref=user_data.genderPref,
        otherColleges=user_data.otherColleges,
        majors=user_data.majors,
        createdAt=datetime.utcnow()
    )
    
    try:
        # Add to database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Delete verification code
        delete_verification_code(user_data.email)
        
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Could not create user. Email may already be registered."
        )

# Login endpoints
@router.post("/login/send-verification", response_model=EmailVerificationResponse)
async def send_login_verification(email: str, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found. Please register first."
        )
    
    # Generate and store verification code
    code = generate_verification_code()
    success = store_verification_code(email, code)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to store verification code. Please try again."
        )
    
    # Send verification email
    sent = send_verification_email(email, code)
    if not sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to send verification email. Please try again."
        )
    
    return EmailVerificationResponse(message="Verification code sent to email", verified=False)

@router.post("/login/verify", response_model=Token)
async def verify_login(email: str, verification_code: str, db: Session = Depends(get_db)):
    # Verify the verification code
    stored_code = get_verification_code(email)
    if not stored_code or stored_code != verification_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid verification code!"
        )
    
    # Get user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found!"
        )
    
    # Generate JWT token
    access_token = create_access_token(data={"sub": user.email})
    
    # Delete the verification code
    delete_verification_code(email)
    
    # Return the token
    return {"access_token": access_token, "token_type": "bearer"}