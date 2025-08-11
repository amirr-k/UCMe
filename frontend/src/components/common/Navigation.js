import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import './Navigation.css';

const Navigation = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const [showUserMenu, setShowUserMenu] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
    setShowUserMenu(false);
  };

  if (!isAuthenticated) {
    return null; // Don't show navigation for unauthenticated users
  }

  return (
    <nav className="navigation">
      <div className="nav-container">
        <Link to="/discover" className="nav-logo">
          UCMe
        </Link>
        
        <div className="nav-links">
          <Link to="/discover" className="nav-link">
            Discover
          </Link>
          <Link to="/matches" className="nav-link">
            Matches
          </Link>
          <Link to="/messages" className="nav-link">
            Messages
          </Link>
          <Link to="/profile" className="nav-link">
            Profile
          </Link>
        </div>
        
        <div className="nav-user">
          <div 
            className="user-menu-trigger"
            onClick={() => setShowUserMenu(!showUserMenu)}
          >
            <div className="user-avatar">
              {user?.name?.charAt(0) || 'U'}
            </div>
            <span className="user-name">{user?.name || 'User'}</span>
            <span className="dropdown-arrow">▼</span>
          </div>
          
          {showUserMenu && (
            <div className="user-menu">
              <div className="user-menu-header">
                <strong>{user?.email}</strong>
                {user?.university && (
                  <div className="user-university">{user.university}</div>
                )}
              </div>
              <div className="user-menu-divider"></div>
              <Link to="/profile" className="user-menu-item">
                Edit Profile
              </Link>
              <Link to="/settings" className="user-menu-item">
                Settings
              </Link>
              <button onClick={handleLogout} className="user-menu-item logout">
                Sign Out
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navigation; 