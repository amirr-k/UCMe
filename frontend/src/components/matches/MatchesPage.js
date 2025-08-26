import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { interactionsService } from '../../services/interactionsService';
import { createConversation } from '../../services/messageService';
import './MatchesPage.css';

const MatchesPage = () => {
  const { token } = useAuth();
  const navigate = useNavigate();
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadMatches();
  }, []);

  const loadMatches = async () => {
    try {
      setLoading(true);
      const data = await interactionsService.getMatches(token);
      setMatches(data);
    } catch (err) {
      setError('Failed to load matches. Please try again.');
      console.error('Error loading matches:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleMessageClick = async (otherUserId) => {
    try {
      const conversation = await createConversation(otherUserId);
      navigate(`/messages/${conversation.id}`);
    } catch (err) {
      console.error('Error starting conversation:', err);
      navigate('/messages');
    }
  };

  const handleProfileClick = (userId) => {
    navigate(`/profile/${userId}`);
  };

  if (loading) {
    return (
      <div className="matches-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading your matches...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="matches-container">
        <div className="error-message">
          <p>{error}</p>
          <button onClick={loadMatches} className="retry-button">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (matches.length === 0) {
    return (
      <div className="matches-container">
        <div className="no-matches">
          <div className="no-matches-icon">💔</div>
          <h2>No Matches Yet</h2>
          <p>Start swiping to find your perfect match!</p>
          <button 
            onClick={() => navigate('/discover')} 
            className="discover-button"
          >
            Go to Discover
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="matches-container">
      <div className="matches-header">
        <h1>Your Matches</h1>
        <p>{matches.length} {matches.length === 1 ? 'match' : 'matches'} found</p>
      </div>

      <div className="matches-grid">
        {matches.map((match) => (
          <div key={match.id} className="match-card">
            <div className="match-image-container">
              {match.user.images && match.user.images.length > 0 ? (
                <img 
                  src={match.user.images.find(img => img.isPrimary)?.imageUrl || match.user.images[0].imageUrl} 
                  alt={match.user.name}
                  className="match-image"
                />
              ) : (
                <div className="match-image-placeholder">
                  <span>{match.user.name?.charAt(0) || 'U'}</span>
                </div>
              )}
              <div className="match-overlay">
                <button 
                  onClick={() => handleMessageClick(match.user.id)}
                  className="message-button"
                >
                  💬 Message
                </button>
                <button 
                  onClick={() => handleProfileClick(match.user.id)}
                  className="profile-button"
                >
                  👤 View Profile
                </button>
              </div>
            </div>

            <div className="match-info">
              <h3>{match.user.name || 'Anonymous'}, {match.user.age || 'N/A'}</h3>
              <p className="match-college">{match.user.college || 'N/A'}</p>
              <p className="match-major">{match.user.major || 'N/A'}</p>
              
              {match.user.interests && match.user.interests.length > 0 && (
                <div className="match-interests">
                  {match.user.interests.slice(0, 3).map((interest, index) => (
                    <span key={index} className="interest-tag">{interest}</span>
                  ))}
                  {match.user.interests.length > 3 && (
                    <span className="interest-more">+{match.user.interests.length - 3} more</span>
                  )}
                </div>
              )}

              <div className="match-actions">
                <button 
                  onClick={() => handleMessageClick(match.user.id)}
                  className="action-button primary"
                >
                  Send Message
                </button>
                <button 
                  onClick={() => handleProfileClick(match.user.id)}
                  className="action-button secondary"
                >
                  View Profile
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MatchesPage; 