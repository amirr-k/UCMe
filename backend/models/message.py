from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Boolean, UniqueConstraint, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import base

class Conversation(base):
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True, index=True)
    userId1 = Column(Integer, ForeignKey('users.id'), nullable=False)
    userId2 = Column(Integer, ForeignKey('users.id'), nullable=False)
    lastMessageAt = Column(DateTime, server_default=func.now(), onupdate=func.now())
    createdAt = Column(DateTime, server_default=func.now())
    
    # Relationships
    user1 = relationship("User", foreign_keys=[userId1], backref="conversations_as_user1")
    user2 = relationship("User", foreign_keys=[userId2], backref="conversations_as_user2")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    
    #Unique constraint to prevent duplicate conversations
    __table_args__ = (
        UniqueConstraint('userId1', 'userId2', name='uq_conversation_participants'),
        CheckConstraint('"userId1" <> "userId2"', name='check_different_users'),
        CheckConstraint('"userId1" < "userId2"', name='check_user_order'),
    )

class Message(base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True, index=True)
    conversationId = Column(Integer, ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False)
    senderId = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    isRead = Column(Boolean, default=False, nullable=False)
    createdAt = Column(DateTime, server_default=func.now())
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    sender = relationship("User", foreign_keys=[senderId], backref="sent_messages")