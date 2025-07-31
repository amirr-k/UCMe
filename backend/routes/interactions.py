from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.swipe import Swipe
from models.match import Match
from schemas.swipe import SwipeCreate, SwipeResponse
from schemas.match import MatchResponse
from utils.jwt_auth import getCurrentUser
from typing import List

router = APIRouter(tags=["Interactions"])

@router.post("/like", response_model=SwipeResponse)
async def likeProfile(
    targetId: int,
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):

    # Verify target user exists and is approved
    targetUser = db.query(User).filter(
        User.id == targetId,
        User.moderationStatus == "Approved"
    ).first()
    
    if not targetUser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent users from liking themselves
    if targetId == currentUser.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot like your own profile"
        )
    
    # Check if user has already liked this profile
    existingSwipe = db.query(Swipe).filter(
        Swipe.userId == currentUser.id,
        Swipe.targetId == targetId
    ).first()
    
    if existingSwipe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already liked this profile"
        )
    
    # Create like record (only likes are stored, not passes)
    newSwipe = Swipe(
        userId=currentUser.id,
        targetId=targetId,
        isLike=True  # Only likes are recorded
    )
    
    try:
        db.add(newSwipe)
        db.commit()
        db.refresh(newSwipe)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to record like"
        )
    
    # Check for mutual like to create match
    mutualSwipe = db.query(Swipe).filter(
        Swipe.userId == targetId,
        Swipe.targetId == currentUser.id,
        Swipe.isLike == True
    ).first()
    
    isMatch = False
    matchId = None
    
    if mutualSwipe:
        # Create match when both users have liked each other
        newMatch = Match(
            userId1=min(currentUser.id, targetId),  # Lower ID always first for consistency
            userId2=max(currentUser.id, targetId)
        )
        try:
            db.add(newMatch)
            db.commit()
            db.refresh(newMatch)
            
            isMatch = True
            matchId = newMatch.id
        except Exception as e:
            # If match creation fails, still return successful like
            print(f"Match creation failed: {e}")
    
    return SwipeResponse(
        id=newSwipe.id,
        targetId=targetId,
        isLike=True,
        isMatch=isMatch,
        matchId=matchId
    )

@router.post("/pass")
async def passProfile(
    targetId: int,
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):
    
    # Verify target user exists (basic validation)
    targetUser = db.query(User).filter(
        User.id == targetId,
        User.moderationStatus == "Approved"
    ).first()
    
    if not targetUser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent users from passing themselves
    if targetId == currentUser.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot pass your own profile"
        )
    
    # NO database record is created for passes - just return success
    # This ensures passes don't affect future recommendations
    return {"message": "Profile passed", "action": "pass", "targetId": targetId}

@router.get("/matches", response_model=List[MatchResponse])
async def getMatches(
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):
  
    # Find all matches where current user is either user1 or user2
    matches = db.query(Match).filter(
        (Match.userId1 == currentUser.id) | (Match.userId2 == currentUser.id)
    ).order_by(Match.createdAt.desc()).all()
    
    result = []
    for match in matches:
        # Determine which user is the "other" user in the match
        otherUserId = match.userId2 if match.userId1 == currentUser.id else match.userId1
        otherUser = db.query(User).filter(
            User.id == otherUserId,
            User.moderationStatus == "Approved"  # Only show matches with approved users
        ).first()
        
        if otherUser:
            result.append(MatchResponse(
                id=match.id,
                createdAt=match.createdAt,
                user=otherUser
            ))
    
    return result

@router.get("/sentLikes", response_model=List[int])
async def getSentLikes(
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):

    likes = db.query(Swipe.targetId).filter(
        Swipe.userId == currentUser.id,
        Swipe.isLike == True
    ).all()
    
    return [like.targetId for like in likes]

@router.get("/receivedLikes", response_model=List[int])
async def getReceivedLikes(
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):

    likes = db.query(Swipe.userId).filter(
        Swipe.targetId == currentUser.id,
        Swipe.isLike == True
    ).all()
    
    return [like.userId for like in likes] 