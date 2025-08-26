import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { recommendationsService } from '../../services/recommendationsService';
import { interactionsService } from '../../services/interactionsService';
import './DiscoverPage.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const DiscoverPage = () => {
  const { token } = useAuth();
  const [recommendations, setRecommendations] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [swipeDirection, setSwipeDirection] = useState(null);
  const [isMatch, setIsMatch] = useState(false);

  useEffect(() => {
    loadRecommendations();
  }, []);

  const loadRecommendations = async () => {
    try {
      setLoading(true);
      const data = await recommendationsService.getDiscoverRecommendations(token);
      setRecommendations(data);
      setCurrentIndex(0);
    } catch (err) {
      setError('Failed to load recommendations. Please try again.');
      console.error('Error loading recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSwipe = async (direction) => {
    if (currentIndex >= recommendations.length) return;

    const currentUser = recommendations[currentIndex];
    setSwipeDirection(direction);

    try {
      if (direction === 'right') {
        const result = await interactionsService.likeProfile(currentUser.id, token);
        if (result.isMatch) {
          setIsMatch(true);
          setTimeout(() => setIsMatch(false), 2000);
        }
      } else {
        await interactionsService.passProfile(currentUser.id, token);
      }
    } catch (err) {
      console.error('Swipe error:', err);
    }

    // Move to next user after a short delay
    setTimeout(() => {
      setCurrentIndex(prev => prev + 1);
      setSwipeDirection(null);
    }, 300);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'ArrowLeft') {
      handleSwipe('left');
    } else if (e.key === 'ArrowRight') {
      handleSwipe('right');
    }
  };

  useEffect(() => {
    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [currentIndex]);

  if (loading) {
    return (
      <div className="discover-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Finding your perfect matches...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="discover-container">
        <div className="error-message">
          <p>{error}</p>
          <button onClick={loadRecommendations} className="retry-button">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (currentIndex >= recommendations.length) {
    return (
      <div className="discover-container">
        <div className="no-more-profiles">
          <h2>No More Profiles</h2>
          <p>You've seen all available profiles for now.</p>
          <p>Check back later for new matches!</p>
          <button onClick={loadRecommendations} className="refresh-button">
            Refresh
          </button>
        </div>
      </div>
    );
  }

  const currentUser = recommendations[currentIndex];
  const primaryImage = currentUser.images?.find(img => img.isPrimary) || currentUser.images?.[0];
  const imageSrc = primaryImage ? (primaryImage.imageUrl.startsWith('http') ? primaryImage.imageUrl : `${API_URL}/${primaryImage.imageUrl}`) : null;

  return (
    <div className="discover-container">
      <div className="discover-header">
        <h1>Discover</h1>
        <p>Swipe right to like, left to pass</p>
      </div>

      <div className="card-container">
        <div 
          className={`profile-card ${swipeDirection ? `swipe-${swipeDirection}` : ''}`}
          key={currentUser.id}
        >
          {imageSrc ? (
            <div className="profile-image">
              <img 
                src={imageSrc}
                alt={currentUser.name || 'User'}
              />
            </div>
          ) : (
            <div className="profile-image-placeholder">
              <span>{currentUser.name?.charAt(0) || 'U'}</span>
            </div>
          )}

          <div className="profile-info">
            <h2>{currentUser.name || 'Anonymous'}, {currentUser.age || 'N/A'}</h2>
            <p className="college">{currentUser.college || 'N/A'}</p>
            <p className="major">{currentUser.major || 'N/A'}</p>
            <div className="profile-info-scroll">
              <p className="bio">{currentUser.bio || 'No bio available'}</p>
              {currentUser.classes && currentUser.classes.length > 0 && (
                <div className="classes">
                  <strong>Classes: </strong>
                  <span>{currentUser.classes.join(', ')}</span>
                </div>
              )}
              {currentUser.interests && currentUser.interests.length > 0 && (
                <div className="interests">
                  {currentUser.interests.map((interest, index) => (
                    <span key={index} className="interest-tag">{interest}</span>
                  ))}
                </div>
              )}
            </div>
          </div>

          <div className="swipe-buttons">
            <button 
              className="swipe-button left"
              onClick={() => handleSwipe('left')}
              aria-label="Pass"
            >
              ✕
            </button>
            <button 
              className="swipe-button right"
              onClick={() => handleSwipe('right')}
              aria-label="Like"
            >
              ♥
            </button>
          </div>
        </div>
      </div>

      {isMatch && (
        <div className="match-notification">
          <h2>It's a Match!</h2>
          <p>You and {currentUser.name || 'Anonymous'} liked each other!</p>
        </div>
      )}
    </div>
  );
};

export default DiscoverPage; 