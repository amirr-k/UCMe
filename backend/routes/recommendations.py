from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_
from database import get_db
from models.user import User
from models.swipe import Swipe
from models.match import Match
from schemas.user import UserResponse
from utils.jwt_auth import getCurrentUser
from typing import List
import random

router = APIRouter(tags=["Recommendations"])

@router.get("/discover", response_model=List[UserResponse])
async def getRecommendations(
    limit: int = 20,
    offset: int = 0,
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):
    
    # Get users that current user has already liked 
    likedUserIds = db.query(Swipe.targetId).filter(
        Swipe.userId == currentUser.id,
        Swipe.isLike == True
    ).subquery()
    
    # Base query for recommendations 
    query = db.query(User).filter(
        User.id != currentUser.id,
        User.moderationStatus == "Approved",
        not_(User.id.in_(likedUserIds))
    )
    
    preferenceFilters = []
    
    
    if currentUser.genderPref and currentUser.genderPref != "Everyone":
        preferenceFilters.append(User.gender == currentUser.genderPref)
    
    if currentUser.minAge and currentUser.maxAge:
        preferenceFilters.append(
            and_(
                User.age >= currentUser.minAge,
                User.age <= currentUser.maxAge
            )
        )
    
    if currentUser.otherColleges and len(currentUser.otherColleges) > 0:
        collegeFilter = or_(
            User.college == currentUser.college,
            User.college.in_(currentUser.otherColleges)
        )
        preferenceFilters.append(collegeFilter)
    else:
        preferenceFilters.append(User.college == currentUser.college)
    
    if currentUser.majors and len(currentUser.majors) > 0:
        preferenceFilters.append(User.major.in_(currentUser.majors))
    
    if preferenceFilters:
        query = query.filter(and_(*preferenceFilters))
    
    mutualCompatibilityFilters = []
    
    mutualCompatibilityFilters.append(
        or_(
            User.genderPref == "Everyone",
            User.genderPref == currentUser.gender,
            User.genderPref.is_(None)  
        )
    )
    
    mutualCompatibilityFilters.append(
        and_(
            or_(User.minAge.is_(None), User.minAge <= currentUser.age),
            or_(User.maxAge.is_(None), User.maxAge >= currentUser.age)
        )
    )
    
    mutualCompatibilityFilters.append(
        or_(
            User.college == currentUser.college,  
            User.otherColleges.any(currentUser.college),  
            User.otherColleges == []  
        )
    )
    
    query = query.filter(and_(*mutualCompatibilityFilters))
    
    allMatchingUsers = query.all()
    
    random.shuffle(allMatchingUsers)
    
    paginatedUsers = allMatchingUsers[offset:offset + limit]
    
    return paginatedUsers

@router.get("/profile/{userId}", response_model=UserResponse)
async def getProfileById(
    userId: int,
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):
    
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
            detail="Use /profile/me endpoint to view your own profile"
        )
    
    existingLike = db.query(Swipe).filter(
        Swipe.userId == currentUser.id,
        Swipe.targetId == userId,
        Swipe.isLike == True
    ).first()
    
    if existingLike:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already liked this profile"
        )
    
    return user

@router.get("/stats")
async def getDiscoveryStats(
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):
    
    # Get users that current user has already liked 
    likedUserIds = db.query(Swipe.targetId).filter(
        Swipe.userId == currentUser.id,
        Swipe.isLike == True
    ).subquery()
    
    availableQuery = db.query(User).filter(
        User.id != currentUser.id,
        User.moderationStatus == "Approved",
        not_(User.id.in_(likedUserIds))
    )
    
    if currentUser.genderPref and currentUser.genderPref != "Everyone":
        availableQuery = availableQuery.filter(User.gender == currentUser.genderPref)
    
    if currentUser.minAge and currentUser.maxAge:
        availableQuery = availableQuery.filter(
            and_(
                User.age >= currentUser.minAge,
                User.age <= currentUser.maxAge
            )
        )
    
    if currentUser.otherColleges and len(currentUser.otherColleges) > 0:
        collegeFilter = or_(
            User.college == currentUser.college,
            User.college.in_(currentUser.otherColleges)
        )
        availableQuery = availableQuery.filter(collegeFilter)
    else:
        availableQuery = availableQuery.filter(User.college == currentUser.college)
    
    totalAvailable = availableQuery.count()
    
    totalLikes = db.query(Swipe).filter(
        Swipe.userId == currentUser.id,
        Swipe.isLike == True
    ).count()
    
    likesReceived = db.query(Swipe).filter(
        Swipe.targetId == currentUser.id,
        Swipe.isLike == True
    ).count()
    
    totalMatches = db.query(Match).filter(
        or_(
            Match.userId1 == currentUser.id,
            Match.userId2 == currentUser.id
        )
    ).count()
    
    return {
        "profilesAvailable": totalAvailable,
        "totalLikes": totalLikes,
        "likesReceived": likesReceived,
        "totalMatches": totalMatches,
        "profilesLiked": totalLikes  
    }

@router.get("/filters")
async def getRecommendationFilters(
    currentUser: User = Depends(getCurrentUser)
):
    """Get current user's recommendation filter preferences"""
    return {
        "genderPref": currentUser.genderPref,
        "minAge": currentUser.minAge,
        "maxAge": currentUser.maxAge,
        "college": currentUser.college,
        "otherColleges": currentUser.otherColleges,
        "majors": currentUser.majors
    } 