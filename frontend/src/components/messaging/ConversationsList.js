// src/components/messaging/ConversationsList.js
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getConversations } from '../../services/messageService';
import '../../styles/messaging/ConversationsList.css';

function ConversationsList() {
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchConversations = async () => {
      setLoading(true);
      try {
        const data = await getConversations();
        setConversations(data);
        setError(null);
      } catch (err) {
        setError('Failed to load conversations');
        console.error('Error loading conversations:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchConversations();
    const intervalId = setInterval(fetchConversations, 30000);
    return () => clearInterval(intervalId);
  }, []);

  if (loading) return <div className="loading">Loading Conversations...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="conversations-container">
      <h2>Messages</h2>
      
      {conversations.length === 0 ? (
        <div className="no-conversations">
          <p>You don't have any conversations yet</p>
          <p>Match with someone new to start one!</p>
        </div>
      ) : (
        <div className="conversations-list">
          {conversations.map(conversation => {
            const { id, otherUser, lastMessage, unreadCount, lastMessageAt } = conversation;
            
            return (
              <Link 
                to={`/messages/${id}`} 
                key={id} 
                className={`conversation-item ${unreadCount > 0 ? 'unread' : ''}`}
              >
                <div className="conversation-avatar">
                  {otherUser.images && otherUser.images.length > 0 ? (
                    <img 
                      src={otherUser.images.find(img => img.isPrimary)?.imageUrl || otherUser.images[0].imageUrl} 
                      alt={`${otherUser.name || 'User'}'s avatar`} 
                    />
                  ) : (
                    <div className="avatar-placeholder">
                      <span>{otherUser.name?.charAt(0) || 'U'}</span>
                    </div>
                  )}
                  {unreadCount > 0 && (
                    <span className="unread-badge">{unreadCount}</span>
                  )}
                </div>
                
                <div className="conversation-details">
                  <div className="conversation-header">
                    <h3>{otherUser.name}</h3>
                    <span className="timestamp">
                      {new Date(lastMessageAt).toLocaleDateString()}
                    </span>
                  </div>
                  
                  <p className="last-message">
                    {lastMessage ? lastMessage.content : 'Start a conversation!'}
                  </p>
                </div>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default ConversationsList;