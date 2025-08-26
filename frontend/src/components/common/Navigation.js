import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";
import "./Navigation.css";

export default function Navigation() {
  const { user, isAuthenticated, logout } = useAuth();
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();

  if (!isAuthenticated) return null;

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="navigation">
      <div className="nav-container">
        <Link to="/discover" className="nav-logo">UCMe</Link>

        <div className="nav-links">
          <Link to="/discover" className="nav-link">Discover</Link>
          <Link to="/matches" className="nav-link">Matches</Link>
          <Link to="/messages" className="nav-link">Messages</Link>
        </div>

        <div className="nav-user">
          <button 
            className="user-menu-trigger" 
            onClick={() => setOpen(!open)}
          >
            <div className="user-avatar">{user?.name?.[0] ?? "U"}</div>
            <span className="user-name">{user?.name ?? "User"}</span>
            <span className="dropdown-arrow">▼</span>
          </button>

          {open && (
            <div className="user-menu">
              <div className="user-menu-header">
                <strong>{user?.email}</strong>
                {user?.university && (
                  <div className="user-university">{user.university}</div>
                )}
              </div>
              <Link to="/profile" className="user-menu-item">Edit Profile</Link>
              <button 
                onClick={handleLogout} 
                className="user-menu-item logout"
              >
                Sign Out
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}