import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import './Login.css'; // Reusing the same styles

const Register = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: '',
    university: '',
    graduationYear: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Basic validation
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters long');
      setLoading(false);
      return;
    }

    try {
      // TODO: Replace with actual API call to your backend
      // For now, we'll simulate a successful registration
      const mockUser = {
        id: 1,
        email: formData.email,
        name: `${formData.firstName} ${formData.lastName}`,
        university: formData.university,
        graduationYear: formData.graduationYear
      };
      
      const mockToken = 'mock-jwt-token-' + Date.now();
      
      // Auto-login after registration
      login(mockUser, mockToken);
      
      // Redirect to discover page
      navigate('/discover', { replace: true });
      
    } catch (err) {
      setError('Registration failed. Please try again.');
      console.error('Registration error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>Join UCMe</h1>
        <p className="subtitle">Create your account to start matching</p>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="firstName">First Name</label>
            <input
              type="text"
              id="firstName"
              name="firstName"
              value={formData.firstName}
              onChange={handleChange}
              placeholder="Enter your first name"
              required
              className="form-input"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="lastName">Last Name</label>
            <input
              type="text"
              id="lastName"
              name="lastName"
              value={formData.lastName}
              onChange={handleChange}
              placeholder="Enter your last name"
              required
              className="form-input"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="email">UC Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="your.email@uc.edu"
              required
              className="form-input"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="university">University</label>
            <select
              id="university"
              name="university"
              value={formData.university}
              onChange={handleChange}
              required
              className="form-input"
            >
              <option value="">Select your university</option>
              <option value="UC Berkeley">UC Berkeley</option>
              <option value="UC Los Angeles">UC Los Angeles</option>
              <option value="UC San Diego">UC San Diego</option>
              <option value="UC Davis">UC Davis</option>
              <option value="UC Irvine">UC Irvine</option>
              <option value="UC Santa Barbara">UC Santa Barbara</option>
              <option value="UC Santa Cruz">UC Santa Cruz</option>
              <option value="UC Riverside">UC Riverside</option>
              <option value="UC Merced">UC Merced</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="graduationYear">Expected Graduation Year</label>
            <select
              id="graduationYear"
              name="graduationYear"
              value={formData.graduationYear}
              onChange={handleChange}
              required
              className="form-input"
            >
              <option value="">Select graduation year</option>
              <option value="2024">2024</option>
              <option value="2025">2025</option>
              <option value="2026">2026</option>
              <option value="2027">2027</option>
              <option value="2028">2028</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Create a password"
              required
              className="form-input"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="Confirm your password"
              required
              className="form-input"
            />
          </div>
          
          <button 
            type="submit" 
            disabled={loading}
            className="login-button"
          >
            {loading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>
        
        <div className="login-footer">
          <p>Already have an account? <a href="/login">Sign in</a></p>
        </div>
      </div>
    </div>
  );
};

export default Register; 