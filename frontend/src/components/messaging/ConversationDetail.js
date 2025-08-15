import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { getConversation, sendMessage } from '../../services/messageService';
import MessageInput from './MessageInput';
import '../../styles/messaging/ConversationDetail.css';

function ConversationDetail() {
  const { conversationId } = useParams();
  const navigate = useNavigate();
  const { user: currentUser } = useAuth();
  const [conversation, setConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchConversation = async () => {
      setLoading(true);
      try {
        const data = await getConversation(conversationId);
        setConversation(data);
        setMessages(data.messages || []);
        setError(null);
      } catch (err) {
        setError('Failed to load conversation');
        console.error('Error loading conversation:', err);
      } finally {
        setLoading(false);
      }
    };

    if (conversationId) {
      fetchConversation();
    }
  }, [conversationId]);

  const handleSendMessage = async (content) => {
    try {
      const newMessage = await sendMessage(conversationId, content);
      setMessages(prev => [...prev, newMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
    }
  };

  if (loading) return <div className="loading">Loading conversation...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!conversation) return <div className="error">Conversation not found</div>;

  return (
    <div className="conversation-detail">
      <div className="conversation-header">
        <button onClick={() => navigate('/messages')} className="back-button">
          ← Back
        </button>
        <h3>{conversation.otherUser?.name || 'Unknown User'}</h3>
      </div>
      
      <div className="messages-container">
        {messages.map((message) => (
          <div 
            key={message.id} 
            className={`message ${message.senderId === currentUser?.id ? 'sent' : 'received'}`}
          >
            <div className="message-content">
              {message.content}
            </div>
            <div className="message-time">
              {new Date(message.createdAt).toLocaleTimeString()}
            </div>
          </div>
        ))}
      </div>
      
      <MessageInput onSendMessage={handleSendMessage} />
    </div>
  );
}

export default ConversationDetail; 