import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import './HomePage.css';

const HomePage = () => {
  const { isAuthenticated, user } = useAuth();

  if (isAuthenticated) {
    return (
      <div className="home-wrap">
        <main className="home-hero">
          <h1 className="home-title">Welcome back{user?.name ? `, ${user.name}` : ''}.</h1>
          <p className="home-lead">
            Pick up where you left off! Discover, match, and message UC students.
          </p>
          <div className="home-actions">
            <Link to="/discover" className="home-button-blue">Continue to Discover</Link>
            <Link to="/matches" className="home-button-gold">View Matches</Link>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="home-wrap">
      <div className="home-grid">
        <main className="home-hero">
          <h1 className="home-title">Meet UC students, not strangers.</h1>
          <p className="home-lead">
            UCMe is a University of California networking platform. 
          </p>
          <p className="home-lead">
            Verify with your .edu email and connect with thousands of students.
            Made by UC students, for UC students.
          </p>

          <ul className="home-bullets" aria-label="Highlights">
            <li> • University of California email verification</li>
            <li> • Preferential, intelligent matching system</li>
            <li> • No bots, no spam, no fake profiles</li>
            <li> • Best of all, no subscription fee</li>
          </ul>

          <div className="home-actions">
            <Link to="/register" className="home-button-blue">Create account</Link>
            <Link to="/login" className="home-button-gold">Sign in</Link>
          </div>
        </main>

        <aside className="home-visual" aria-hidden="true">
          <img src="/images/University_of_California_Logo.svg" alt="University of California logo" />
        </aside>
      </div>
    </div>
  );
};

export default HomePage;