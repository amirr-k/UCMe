from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, func
from database import get_db
from models.user import User
from models.match import Match
from models.message import Conversation, Message
from schemas.message import MessageCreate, MessageResponse, ConversationCreate, ConversationSummary, ConversationDetail, getConversationDetail
from utils.jwt_auth import getCurrentUser
from typing import List

router = APIRouter(tags=["Messages"])

@router.post("/conversations", response_model=ConversationDetail)
async def createConversation(
    conversation: ConversationCreate,
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):
    # Check if target user exists 
    targetUser = db.query(User).filter(
        User.id == conversation.userId2,
        User.moderationStatus == "Approved"
    ).first()
    
    if not targetUser:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Check if users are matched
    isMatched = db.query(Match).filter(
        or_(
            and_(Match.userId1 == currentUser.id, Match.userId2 == conversation.userId2),
            and_(Match.userId1 == conversation.userId2, Match.userId2 == currentUser.id)
        )
    ).first() is not None
    
    if not isMatched:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only start conversations with users you've matched with"
        )
    
    # Ensure userId1 < userId2 for consistency
    userId1 = min(currentUser.id, conversation.userId2)
    userId2 = max(currentUser.id, conversation.userId2)
    
    # Check if conversation already exists
    existingConversation = db.query(Conversation).filter(
        Conversation.userId1 == userId1,
        Conversation.userId2 == userId2
    ).first()
    
    if existingConversation:
        return get_conversation_detail(existingConversation.id, currentUser, db)
    
    # If it doesn't exist, create a new conversation
    newConversation = Conversation(userId1=userId1, userId2=userId2)
    
    try:
        db.add(newConversation)
        db.commit()
        db.refresh(newConversation)
        return getConversationDetail(newConversation.id, currentUser, db)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create conversation: {str(e)}")
    
#Gets details of a specific conversation
@router.get("/conversations/{conversationId}", response_model=ConversationDetail)
async def getConversation(
    conversationId: int,
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):
    return getConversationDetail(conversationId, currentUser, db)