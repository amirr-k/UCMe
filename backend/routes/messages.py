from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, func
from database import get_db
from models.user import User
from models.match import Match
from models.message import Conversation, Message
from schemas.message import MessageCreate, MessageResponse, ConversationCreate, ConversationSummary, ConversationDetail
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
        return getConversationDetail(existingConversation.id, currentUser, db)
    
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
    
# Gets details/summary of a specific conversation
@router.get("/conversations/{conversationId}", response_model=ConversationDetail)
async def getConversation(
    conversationId: int,
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):
    return getConversationDetail(conversationId, currentUser, db)

def getConversationDetail(conversationId, currentUser, db):
    conversation = db.query(Conversation).filter(
        Conversation.id == conversationId,
        or_(
            Conversation.userId1 == currentUser.id,
            Conversation.userId2 == currentUser.id
        )
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    otherUserId = conversation.userId2 if conversation.userId1 == currentUser.id else conversation.userId1
    otherUser = db.query(User).filter(User.id == otherUserId).first()
    
    if not otherUser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Other participant not found"
        )
    
    messages = db.query(Message).filter(
        Message.conversationId == conversationId
    ).order_by(Message.createdAt.asc()).all()
    
    unreadCount = db.query(func.count(Message.id)).filter(
        Message.conversationId == conversationId,
        Message.senderId != currentUser.id,
        Message.isRead == False
    ).scalar()
    
    lastMessage = db.query(Message).filter(
        Message.conversationId == conversationId
    ).order_by(Message.createdAt.desc()).first()
    
    return ConversationDetail(
        id=conversation.id,
        userId1=conversation.userId1,
        userId2=conversation.userId2,
        lastMessageAt=conversation.lastMessageAt,
        createdAt=conversation.createdAt,
        messages=messages,
        lastMessage=lastMessage,
        otherUser=otherUser,
        unreadCount=unreadCount
    )

# Gets list of conversations for current user
@router.get("/conversations", response_model=List[ConversationSummary])
async def listConversations(
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 20):  
    conversations = db.query(Conversation).filter(
        or_(
            Conversation.userId1 == currentUser.id,
            Conversation.userId2 == currentUser.id
        )
    ).order_by(Conversation.lastMessageAt.desc()).offset(skip).limit(limit).all()
    result = []
    for convo in conversations:
        otherUserId = convo.userId2 if convo.userId1 == currentUser.id else convo.userId1
        otherUser = db.query(User).filter(User.id == otherUserId).first()
        if otherUser:
            lastMessage = db.query(Message).filter(
                Message.conversationId == convo.id).order_by(Message.createdAt.desc()).first()
            unreadCount = db.query(func.count(Message.id)).filter(
                Message.conversationId == convo.id,
                Message.senderId != currentUser.id,
                Message.isRead == False
            ).scalar()
            result.append(ConversationSummary(
                id=convo.id,
                userId1=convo.userId1,
                userId2=convo.userId2,
                lastMessageAt=convo.lastMessageAt,
                createdAt=convo.createdAt,
                lastMessage=lastMessage,
                otherUser=otherUser,
                unreadCount=unreadCount))
    return result


# Send a message
@router.post("/conversations/{conversationId}/messages", response_model=MessageResponse)
async def sendMessage(
    conversationId: int,
    message: MessageCreate,
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):
    
    # Check if conversation exists and if user is a participant
    conversation = db.query(Conversation).filter(
        Conversation.id == conversationId,
        or_(
            Conversation.userId1 == currentUser.id,
            Conversation.userId2 == currentUser.id
        )
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or you're not a participant"
        )
    
    # Create new message
    newMessage = Message(
        conversationId=conversationId,
        senderId=currentUser.id,
        content=message.content,
        isRead=False
    )
    
    try:
        db.add(newMessage)
        # Update conversation's lastMessageAt
        conversation.lastMessageAt = func.now()
        db.commit()
        db.refresh(newMessage)
        return newMessage
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send message"
        )
    
# Reading messages
@router.put("/conversations/{conversationId}/read")
async def markConversationAsRead(
    conversationId: int,
    currentUser: User = Depends(getCurrentUser),
    db: Session = Depends(get_db)
):
    
    # Check if conversation exists and if user is a participant
    # Honestly I should probably make this a separate function this is getting
    # repetitive -- note to self lol
    conversation = db.query(Conversation).filter(
        Conversation.id == conversationId,
        or_(
            Conversation.userId1 == currentUser.id,
            Conversation.userId2 == currentUser.id
        )
    ).first()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or you're not a participant"
        )
    
    try:
        # Mark all messages from the other user as read
        db.query(Message).filter(
            Message.conversationId == conversationId,
            Message.senderId != currentUser.id,
            Message.isRead == False
        ).update({"isRead": True})
        
        db.commit()
        return {"message": "All messages marked as read"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to mark messages as read"
        )
    
