import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import './HomePage.css';

const HomePage = () => {
  const { isAuthenticated, user } = useAuth();

  if (isAuthenticated) {
    return (
      <div className="home-container">
        <div className="home-content">
          <h1>Welcome back, {user?.name || 'User'}! 👋</h1>
          <p className="home-subtitle">
            Ready to discover new connections at {user?.university || 'UC'}?
          </p>
          
          <div className="home-actions">
            <Link to="/discover" className="home-button primary">
              Start Discovering
            </Link>
            <Link to="/matches" className="home-button secondary">
              View Matches
            </Link>
          </div>
          
          <div className="home-stats">
            <div className="stat-card">
              <div className="stat-number">0</div>
              <div className="stat-label">New Matches</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">0</div>
              <div className="stat-label">Unread Messages</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">0</div>
              <div className="stat-label">Profile Views</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="home-container">
      <div className="home-content">
        <h1>Welcome to UCMe</h1>
        <p className="home-subtitle">
          The dating app exclusively for UC students. Connect with fellow students 
          who share your academic journey and life goals.
        </p>
        
        <div className="home-features">
          <div className="feature">
            <div className="feature-icon">🎓</div>
            <h3>UC Students Only</h3>
            <p>Connect with verified UC students from all campuses</p>
          </div>
          <div className="feature">
            <div className="feature-icon">💝</div>
            <h3>Smart Matching</h3>
            <p>Match with students who share your academic journey and life goals</p>
          </div>
          <div className="feature">
            <div className="feature-icon">🔒</div>
            <h3>Safe & Secure</h3>
            <p>Your privacy and safety are our top priorities</p>
          </div>
        </div>
        
        <div className="home-actions">
          <Link to="/register" className="home-button primary">
            Get Started
          </Link>
          <Link to="/login" className="home-button secondary">
            Sign In
          </Link>
        </div>
        
        <div className="home-footer">
          <p>Join thousands of UC students finding meaningful connections</p>
        </div>
      </div>
    </div>
  );
};

export default HomePage; 