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
    """Get user recommendations for endless scroll interface - filters out only liked users"""
    
    # Get users that current user has already liked (passes are not stored in database)
    likedUserIds = db.query(Swipe.targetId).filter(
        Swipe.userId == currentUser.id,
        Swipe.isLike == True
    ).subquery()
    
    # Base query for recommendations - exclude self, non-approved users, and already liked users
    query = db.query(User).filter(
        User.id != currentUser.id,
        User.moderationStatus == "Approved",
        not_(User.id.in_(likedUserIds))
    )
    
    # Apply user's preference filters
    preferenceFilters = []
    
    # Gender preference filtering
    if currentUser.genderPref and currentUser.genderPref != "Everyone":
        preferenceFilters.append(User.gender == currentUser.genderPref)
    
    # Age preference filtering
    if currentUser.minAge and currentUser.maxAge:
        preferenceFilters.append(
            and_(
                User.age >= currentUser.minAge,
                User.age <= currentUser.maxAge
            )
        )
    
    # College preference filtering
    if currentUser.otherColleges and len(currentUser.otherColleges) > 0:
        # User wants to see profiles from their college + other specified colleges
        collegeFilter = or_(
            User.college == currentUser.college,
            User.college.in_(currentUser.otherColleges)
        )
        preferenceFilters.append(collegeFilter)
    else:
        # User only wants to see profiles from their own college
        preferenceFilters.append(User.college == currentUser.college)
    
    # Major preference filtering
    if currentUser.majors and len(currentUser.majors) > 0:
        # User has specified preferred majors
        preferenceFilters.append(User.major.in_(currentUser.majors))
    
    # Apply all preference filters
    if preferenceFilters:
        query = query.filter(and_(*preferenceFilters))
    
    # Apply mutual compatibility filtering (they would also be interested in current user)
    mutualCompatibilityFilters = []
    
    # Check if current user matches their gender preference
    mutualCompatibilityFilters.append(
        or_(
            User.genderPref == "Everyone",
            User.genderPref == currentUser.gender,
            User.genderPref.is_(None)  # Handle users who haven't set preference
        )
    )
    
    # Check if current user is in their age range
    mutualCompatibilityFilters.append(
        and_(
            or_(User.minAge.is_(None), User.minAge <= currentUser.age),
            or_(User.maxAge.is_(None), User.maxAge >= currentUser.age)
        )
    )
    
    # Check college compatibility - they should be open to current user's college
    mutualCompatibilityFilters.append(
        or_(
            User.college == currentUser.college,  # Same college
            User.otherColleges.any(currentUser.college),  # Current user's college in their preferences
            User.otherColleges == []  # No specific college preferences (open to all)
        )
    )
    
    # Apply mutual compatibility filters
    query = query.filter(and_(*mutualCompatibilityFilters))
    
    # Get all matching users for randomization
    allMatchingUsers = query.all()
    
    # Shuffle for variety in recommendations
    random.shuffle(allMatchingUsers)
    
    # Apply pagination after shuffling
    paginatedUsers = allMatchingUsers[offset:offset + limit]
    
    return paginatedUsers

@router.get("/profile/{userId}", response_model=UserResponse)
async def getProfileById(
    userId: int,
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):
    """Get a specific user profile by ID - for viewing recommended profiles"""
    
    user = db.query(User).filter(
        User.id == userId,
        User.moderationStatus == "Approved"
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Prevent viewing own profile through this endpoint
    if user.id == currentUser.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use /profile/me endpoint to view your own profile"
        )
    
    # Check if current user has already liked this profile
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
    """Get discovery statistics for current user"""
    
    # Get users that current user has already liked (passes not stored)
    likedUserIds = db.query(Swipe.targetId).filter(
        Swipe.userId == currentUser.id,
        Swipe.isLike == True
    ).subquery()
    
    # Count total available profiles matching user preferences
    availableQuery = db.query(User).filter(
        User.id != currentUser.id,
        User.moderationStatus == "Approved",
        not_(User.id.in_(likedUserIds))
    )
    
    # Apply same filters as recommendation system for accurate count
    if currentUser.genderPref and currentUser.genderPref != "Everyone":
        availableQuery = availableQuery.filter(User.gender == currentUser.genderPref)
    
    if currentUser.minAge and currentUser.maxAge:
        availableQuery = availableQuery.filter(
            and_(
                User.age >= currentUser.minAge,
                User.age <= currentUser.maxAge
            )
        )
    
    # College filtering
    if currentUser.otherColleges and len(currentUser.otherColleges) > 0:
        collegeFilter = or_(
            User.college == currentUser.college,
            User.college.in_(currentUser.otherColleges)
        )
        availableQuery = availableQuery.filter(collegeFilter)
    else:
        availableQuery = availableQuery.filter(User.college == currentUser.college)
    
    totalAvailable = availableQuery.count()
    
    # Count total likes sent by user
    totalLikes = db.query(Swipe).filter(
        Swipe.userId == currentUser.id,
        Swipe.isLike == True
    ).count()
    
    # Count likes received by user
    likesReceived = db.query(Swipe).filter(
        Swipe.targetId == currentUser.id,
        Swipe.isLike == True
    ).count()
    
    # Count total matches
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
        "profilesLiked": totalLikes  # For clarity
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