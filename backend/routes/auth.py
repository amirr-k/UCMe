from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserCreate, UserResponse, EmailVerificationRequest, EmailVerificationResponse, Token
from utils.auth import generateVerificationCode, storeVerificationCode, getVerificationCode, deleteVerificationCode, sendVerificationEmail
from utils.jwt_auth import createAccessToken
from sqlalchemy.exc import IntegrityError
from datetime import datetime

router = APIRouter(tags=["Authentication"])

UC_EMAIL_DOMAINS = {
    "@ucla.edu", "@berkeley.edu", "@ucsd.edu", "@ucsb.edu", "@uci.edu",
    "@ucr.edu", "@ucsc.edu", "@ucdavis.edu", "@ucmerced.edu"
}

def validateUCEmail(email: str) -> bool:
    return any(email.endswith(domain) for domain in UC_EMAIL_DOMAINS)

@router.post("/register/sendVerification", response_model=EmailVerificationResponse)
async def sendRegistrationVerification(email: str, db: Session = Depends(get_db)):
    if not validateUCEmail(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please use a valid UC email address"
        )
    
    existingUser = db.query(User).filter(User.email == email).first()
    if existingUser:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Email already registered! Please login instead"
        )
    
    # Generate and store verification code
    code = generateVerificationCode()
    if not storeVerificationCode(email, code):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate verification code"
        )
    
    if not sendVerificationEmail(email, code):
        deleteVerificationCode(email)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email"
        )
    
    return EmailVerificationResponse(message="Verification code sent", verified=False)

@router.post("/register", response_model=UserResponse)
async def register(userData: UserCreate, db: Session = Depends(get_db)):
    #Verify verification code
    storedCode = getVerificationCode(userData.email)
    if not storedCode or storedCode != userData.verificationCode:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code"
        )
    
    newUser = User(
        email=userData.email,
        name=userData.name,
        college=userData.college,
        school=userData.school,
        year=userData.year,
        gender=userData.gender,
        major=userData.major,
        age=userData.age,
        bio=userData.bio,
        interests=userData.interests,
        classes=userData.classes,
        lookingFor=userData.lookingFor,
        smokes=userData.smokes,
        drinks=userData.drinks,
        pronouns=userData.pronouns,
        location=userData.location,
        hometown=userData.hometown,
        minAge=userData.minAge, 
        maxAge=userData.maxAge,  
        genderPref=userData.genderPref,
        otherColleges=userData.otherColleges,
        majors=userData.majors,
        moderationStatus="Approved"
    )
    
    try:
        # Add to database
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        deleteVerificationCode(userData.email)
        return newUser
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Could not create user"
        )

@router.post("/login/sendVerification", response_model=EmailVerificationResponse)
async def sendLoginVerification(email: str, db: Session = Depends(get_db)):
    #Check if user exists
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found. Please register first"
        )
    
    # Generate and store verification code
    code = generateVerificationCode()
    if not storeVerificationCode(email, code):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate verification code"
        )
    
    if not sendVerificationEmail(email, code):
        deleteVerificationCode(email)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email"
        )
    
    return EmailVerificationResponse(message="Verification code sent to email", verified=False)

@router.post("/login", response_model=Token)
async def login(request: EmailVerificationRequest, db: Session = Depends(get_db)):
    storedCode = getVerificationCode(request.email)
    if not storedCode or storedCode != request.verificationCode:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid verification code!"
        )
    
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    accessToken = createAccessToken(data={"sub": user.email})
    deleteVerificationCode(request.email)
    
    return Token(accessToken=accessToken, tokenType="bearer")

@router.post("/resendVerification", response_model=EmailVerificationResponse)
async def resendVerification(email: str, db: Session = Depends(get_db)):
    if not validateUCEmail(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please use a valid UC email address"
        )
    
    code = generateVerificationCode()
    if not storeVerificationCode(email, code):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate verification code"
        )
    
    if not sendVerificationEmail(email, code):
        deleteVerificationCode(email)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email"
        )
    
    return EmailVerificationResponse(message="Verification code resent", verified=False)