from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from typing import List
from database import get_db
from models.user import User
from models.swipe import Swipe
from models.match import Match
from schemas.user import UserResponse, UserProfileUpdate, UserPreferencesUpdate
from schemas.swipe import SwipeCreate, SwipeResponse
from schemas.match import MatchResponse, MatchUserResponse
from utils.jwt_auth import getCurrentUser

#All routes start with /profile
router = APIRouter(tags=["Profile"], prefix="/profile")

#Get current user's profile
@router.get("/me", response_model=UserResponse)
def getUserProfile(currentUser: User = Depends(getCurrentUser)):
    return currentUser

#Get another user's profile by ID
@router.get("/{userID}", response_model=UserResponse)
def getUserProfile(userID: int, db: Session = Depends(get_db), currentUser: User = Depends(getCurrentUser)):
    user = db.query(User).filter(User.id == userID).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return user

#Update user profile
@router.put("/update", response_model=UserResponse)
def updateProfile(profileData: UserProfileUpdate, db: Session = Depends(get_db), currentUser: User = Depends(getCurrentUser)):
    for key, value in profileData.dict(exclude_unset=True).items():
        setattr(currentUser, key, value)
    
    db.commit()
    db.refresh(currentUser)
    return currentUser

#Update user preferences
@router.put("/preferences", response_model=UserResponse)
def updatePreferences(preferencesData: UserPreferencesUpdate,db: Session = Depends(get_db), currentUser: User = Depends(getCurrentUser)):
    for key, value in preferencesData.dict(exclude_unset=True).items():
        setattr(currentUser, key, value)
    
    db.commit()
    db.refresh(currentUser)
    return currentUser

# Get profiles for swiping (recommendations)
@router.get("/recommendations", response_model=List[UserResponse])
def getRecommendations(limit: int = 10, db: Session = Depends(get_db), currentUser: User = Depends(getCurrentUser)):
    #Get IDs of users that current user has already swiped on
    alreadySwiped = db.query(Swipe.targetId).filter(Swipe.userId == currentUser.id)
    
    #Exclude current user and already swiped profiles
    query = db.query(User).filter(User.id != currentUser.id,User.id.notin_(alreadySwiped))
    
    #Apply preference filters if they exist
    if currentUser.genderPref:
        query = query.filter(User.gender == currentUser.genderPref)
    
    if currentUser.minAge and currentUser.maxAge:
        query = query.filter(and_(User.age >= currentUser.minAge, User.age <= currentUser.maxAge))
    
    if currentUser.otherColleges:
        query = query.filter(or_(User.college == currentUser.college, User.college.in_(currentUser.otherColleges)))
    
    if currentUser.majors:query = query.filter(User.major.in_(currentUser.majors))
    
    #Order by random to provide variety in recommendations
    query = query.order_by(func.random())
    
    #Limit results
    recommendations = query.limit(limit).all()
    
    return recommendations

#Record swipes
@router.post("/swipe", response_model=SwipeResponse)
def createSwipe(swipeData: SwipeCreate,db: Session = Depends(get_db),currentUser: User = Depends(getCurrentUser)):
    targetUser = db.query(User).filter(User.id == swipeData.targetId).first()
    if not targetUser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target user not found"
        )
    
    #Check if already swiped on this user
    existingSwipe = db.query(Swipe).filter(Swipe.userId == currentUser.id,Swipe.targetId == swipeData.targetId).first()
    
    if existingSwipe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already swiped on this user"
        )
    
    #Create new swipe record
    newSwipe = Swipe(userId=currentUser.id,targetId=swipeData.targetId,isLike=swipeData.isLike)
    
    db.add(newSwipe)
    db.commit()
    db.refresh(newSwipe)
    
    #Check if this creates a match (both users liked each other)
    isMatch = False
    matchId = None
    
    if swipeData.isLike:
        # Check if the other person also liked current user
        otherSwipe = db.query(Swipe).filter(Swipe.userId == swipeData.targetId, Swipe.targetId == currentUser.id,Swipe.isLike == True).first()
        
        if otherSwipe:
            isMatch = True
            
            #Create a match record
            userId1, userId2 = sorted([currentUser.id, swipeData.targetId])
            
            #Check if match already exists
            existingMatch = db.query(Match).filter(Match.userId1 == userId1,Match.userId2 == userId2).first()
            
            if not existingMatch:
                newMatch = Match(userId1=userId1,userId2=userId2)
                db.add(newMatch)
                db.commit()
                db.refresh(newMatch)
                matchId = newMatch.id
            else:
                matchId = existingMatch.id
    
    return {
        "id": newSwipe.id,
        "targetId": newSwipe.targetId,
        "isLike": newSwipe.isLike,
        "isMatch": isMatch,
        "matchId": matchId
    }

#Get all matches for current user
@router.get("/matches", response_model=List[MatchUserResponse])
def getMatches(db: Session = Depends(get_db),currentUser: User = Depends(getCurrentUser)):
    matches = db.query(Match).filter(or_(Match.userId1 == currentUser.id,Match.userId2 == currentUser.id)).order_by(Match.createdAt.desc()).all()
    
    result = []
    for match in matches:
        otherUserId = match.userId2 if match.userId1 == currentUser.id else match.userId1
        otherUser = db.query(User).filter(User.id == otherUserId).first()
        
        if otherUser:
            result.append({"matchId": match.id,"createdAt": match.createdAt,"user": otherUser})
    
    return result

#Get a specific match by ID
@router.get("/matches/{matchId}", response_model=MatchResponse)
def getMatch(matchId: int,db: Session = Depends(get_db),currentUser: User = Depends(getCurrentUser)):
    match = db.query(Match).filter(Match.id == matchId,or_(Match.userId1 == currentUser.id,Match.userId2 == currentUser.id)).first()
    
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    otherUserId = match.userId2 if match.userId1 == currentUser.id else match.userId1
    
    otherUser = db.query(User).filter(User.id == otherUserId).first()
    
    return {
        "id": match.id,
        "createdAt": match.createdAt,
        "user": otherUser
    }

#Unmatch with a user
@router.delete("/matches/{matchId}", status_code=status.HTTP_204_NO_CONTENT)
def deleteMatch(matchId: int,db: Session = Depends(get_db),currentUser: User = Depends(getCurrentUser)):
    match = db.query(Match).filter(
        Match.id == matchId,
        or_(
            Match.userId1 == currentUser.id,
            Match.userId2 == currentUser.id
        )
    ).first()
    
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )
    
    db.delete(match)
    db.commit()
    
    return None