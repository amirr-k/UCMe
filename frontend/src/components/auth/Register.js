import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { authService } from '../../services/authService';
import './Login.css';

const UC_CAMPUSES = [
  'UC Berkeley',
  'UC Los Angeles',
  'UC San Diego',
  'UC Davis',
  'UC Irvine',
  'UC Santa Barbara',
  'UC Santa Cruz',
  'UC Riverside',
  'UC Merced'
];

const YEARS = [2024, 2025, 2026, 2027, 2028, 2029, 2030];

const Register = () => {
  const [step, setStep] = useState('email'); // 'email' | 'verify' | 'profile'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [countdown, setCountdown] = useState(0);

  const [email, setEmail] = useState('');
  const [verificationCode, setVerificationCode] = useState('');

  // Step 3 - Profile form
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    college: '',
    school: '',
    year: '',
    age: '',
    gender: '',
    major: '',
    bio: '',
    interests: '', // comma-separated
    classes: '', // comma-separated (optional)
    lookingFor: 'Dating',
    smokes: false,
    drinks: false,
    pronouns: '',
    location: '',
    hometown: '',
    minAge: '',
    maxAge: '',
    genderPref: 'Any',
    otherColleges: '', // comma-separated (optional)
    majors: '' // comma-separated (optional)
  });


  const navigate = useNavigate();

  useEffect(() => {
    if (countdown > 0) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [countdown]);

  const handleRequestCode = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await authService.requestRegistrationCode(email);
      setStep('verify');
      setCountdown(60);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to send verification code. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleResendCode = async () => {
    if (countdown > 0) return;
    setLoading(true);
    setError('');
    try {
      await authService.resendVerificationCode(email);
      setCountdown(60);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to resend code. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyContinue = (e) => {
    e.preventDefault();
    if (!verificationCode || verificationCode.length !== 6) {
      setError('Please enter the 6-digit verification code sent to your email.');
      return;
    }
    setError('');
    setStep('profile');
  };

  const onFieldChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const parseCsv = (text) => {
    if (!text) return [];
    return text
      .split(',')
      .map((s) => s.trim())
      .filter((s) => s.length > 0);
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Basic validations matching backend schema constraints
    if (!formData.firstName || !formData.lastName) {
      setError('Please provide your first and last name.');
      setLoading(false);
      return;
    }
    if (!formData.college || !formData.school || !formData.year || !formData.age) {
      setError('Please complete college, school, graduation year, and age.');
      setLoading(false);
      return;
    }
    if (!formData.gender || !formData.major || !formData.bio) {
      setError('Please complete gender, major, and bio.');
      setLoading(false);
      return;
    }
    const interests = parseCsv(formData.interests);
    if (interests.length < 1) {
      setError('Please provide at least one interest.');
      setLoading(false);
      return;
    }
    if (!formData.minAge || !formData.maxAge) {
      setError('Please set your preferred age range.');
      setLoading(false);
      return;
    }
    if (Number(formData.maxAge) < Number(formData.minAge)) {
      setError('Max age must be greater than or equal to min age.');
      setLoading(false);
      return;
    }

    try {
      const payload = {
        email,
        name: `${formData.firstName} ${formData.lastName}`.trim(),
        college: formData.college,
        school: formData.school,
        year: Number(formData.year),
        age: Number(formData.age),
        gender: formData.gender,
        major: formData.major,
        verificationCode,
        bio: formData.bio,
        interests,
        classes: parseCsv(formData.classes),
        lookingFor: formData.lookingFor,
        smokes: Boolean(formData.smokes),
        drinks: Boolean(formData.drinks),
        pronouns: formData.pronouns,
        location: formData.location,
        hometown: formData.hometown,
        minAge: Number(formData.minAge),
        maxAge: Number(formData.maxAge),
        genderPref: formData.genderPref,
        otherColleges: parseCsv(formData.otherColleges),
        majors: parseCsv(formData.majors)
      };

      await authService.register(payload);

      // After successful registration, redirect to login page
      navigate('/login', { replace: true, state: { email } });
    } catch (err) {
      setError(err?.response?.data?.detail || 'Registration failed. Please review your info and try again.');
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

        {step === 'email' && (
          <form onSubmit={handleRequestCode} className="login-form">
            <div className="form-group">
              <label htmlFor="email">UC Email</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Example: amirkiadi@ucsd.edu"
                required
                className="form-input"
                disabled={loading}
              />
            </div>

            <button type="submit" disabled={loading} className="login-button">
              {loading ? 'Sending Code...' : 'Get Verification Code'}
            </button>
          </form>
        )}

        {step === 'verify' && (
          <form onSubmit={handleVerifyContinue} className="login-form">
            <div className="form-group">
              <label htmlFor="verificationCode">Verification Code</label>
              <input
                type="text"
                id="verificationCode"
                value={verificationCode}
                onChange={(e) => setVerificationCode(e.target.value)}
                placeholder="Enter 6-digit code"
                required
                className="form-input"
                disabled={loading}
                maxLength={6}
              />
              <div className="verification-help">
                <p>A verification code has been sent to {email}</p>
                <button
                  type="button"
                  onClick={handleResendCode}
                  className="resend-button"
                  disabled={countdown > 0 || loading}
                >
                  {countdown > 0 ? `Resend code in ${countdown}s` : 'Resend code'}
                </button>
                <button
                  type="button"
                  onClick={() => setStep('email')}
                  className="back-button"
                  disabled={loading}
                >
                  Use different email
                </button>
              </div>
            </div>

            <button type="submit" disabled={loading || verificationCode.length !== 6} className="login-button">
              Continue
            </button>
          </form>
        )}

        {step === 'profile' && (
          <form onSubmit={handleRegister} className="login-form">
            <div className="form-group">
              <label htmlFor="firstName">First Name</label>
              <input
                type="text"
                id="firstName"
                name="firstName"
                value={formData.firstName}
                onChange={onFieldChange}
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
                onChange={onFieldChange}
                placeholder="Enter your last name"
                required
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="college">UC Campus</label>
              <select
                id="college"
                name="college"
                value={formData.college}
                onChange={onFieldChange}
                required
                className="form-input"
              >
                <option value="">Select your campus</option>
                {UC_CAMPUSES.map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="school">School</label>
              <input
                type="text"
                id="school"
                name="school"
                value={formData.school}
                onChange={onFieldChange}
                placeholder="e.g., College of Engineering"
                required
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="year">Graduation Year</label>
              <select
                id="year"
                name="year"
                value={formData.year}
                onChange={onFieldChange}
                required
                className="form-input"
              >
                <option value="">Select graduation year</option>
                {YEARS.map((y) => (
                  <option key={y} value={y}>{y}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="age">Age</label>
              <input
                type="number"
                id="age"
                name="age"
                value={formData.age}
                onChange={onFieldChange}
                min="18"
                max="100"
                required
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="gender">Gender</label>
              <input
                type="text"
                id="gender"
                name="gender"
                value={formData.gender}
                onChange={onFieldChange}
                placeholder="Your gender"
                required
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="major">Major</label>
              <input
                type="text"
                id="major"
                name="major"
                value={formData.major}
                onChange={onFieldChange}
                placeholder="Your major"
                required
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="bio">Bio</label>
              <textarea
                id="bio"
                name="bio"
                value={formData.bio}
                onChange={onFieldChange}
                placeholder="Tell us about yourself (10-500 chars)"
                required
                className="form-input"
                rows={3}
              />
            </div>

            <div className="form-group">
              <label htmlFor="interests">Interests (comma-separated)</label>
              <input
                type="text"
                id="interests"
                name="interests"
                value={formData.interests}
                onChange={onFieldChange}
                placeholder="e.g., hiking, movies, coding"
                required
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="classes">Classes (optional, comma-separated)</label>
              <input
                type="text"
                id="classes"
                name="classes"
                value={formData.classes}
                onChange={onFieldChange}
                placeholder="e.g., CS61A, MATH1B"
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="lookingFor">Looking For</label>
              <select
                id="lookingFor"
                name="lookingFor"
                value={formData.lookingFor}
                onChange={onFieldChange}
                required
                className="form-input"
              >
                <option>Dating</option>
                <option>Friends</option>
                <option>Networking</option>
              </select>
            </div>

            <div className="form-group">
              <label>Habits</label>
              <div style={{ display: 'flex', gap: 12 }}>
                <label><input type="checkbox" name="smokes" checked={formData.smokes} onChange={onFieldChange} /> Smokes</label>
                <label><input type="checkbox" name="drinks" checked={formData.drinks} onChange={onFieldChange} /> Drinks</label>
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="pronouns">Pronouns</label>
              <input
                type="text"
                id="pronouns"
                name="pronouns"
                value={formData.pronouns}
                onChange={onFieldChange}
                placeholder="e.g., she/her, he/him, they/them"
                required
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="location">Current Location</label>
              <input
                type="text"
                id="location"
                name="location"
                value={formData.location}
                onChange={onFieldChange}
                placeholder="City, State"
                required
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="hometown">Hometown</label>
              <input
                type="text"
                id="hometown"
                name="hometown"
                value={formData.hometown}
                onChange={onFieldChange}
                placeholder="City, State"
                required
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label>Preferred Age Range</label>
              <div style={{ display: 'flex', gap: 12 }}>
                <input
                  type="number"
                  name="minAge"
                  value={formData.minAge}
                  onChange={onFieldChange}
                  min="18"
                  max="100"
                  placeholder="Min"
                  required
                  className="form-input"
                />
                <input
                  type="number"
                  name="maxAge"
                  value={formData.maxAge}
                  onChange={onFieldChange}
                  min="18"
                  max="100"
                  placeholder="Max"
                  required
                  className="form-input"
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="genderPref">Preferred Gender</label>
              <select
                id="genderPref"
                name="genderPref"
                value={formData.genderPref}
                onChange={onFieldChange}
                required
                className="form-input"
              >
                <option>Any</option>
                <option>Women</option>
                <option>Men</option>
                <option>Non-binary</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="otherColleges">Other UC Campuses to See (optional, comma-separated)</label>
              <input
                type="text"
                id="otherColleges"
                name="otherColleges"
                value={formData.otherColleges}
                onChange={onFieldChange}
                placeholder="e.g., UC San Diego, UC Davis"
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="majors">Preferred Majors (optional, comma-separated)</label>
              <input
                type="text"
                id="majors"
                name="majors"
                value={formData.majors}
                onChange={onFieldChange}
                placeholder="e.g., CS, Biology, Economics"
                className="form-input"
              />
            </div>

            <button type="submit" disabled={loading} className="login-button">
              {loading ? 'Creating Account...' : 'Create Account'}
            </button>
          </form>
        )}

        <div className="login-footer">
          <p>Already have an account? <a href="/login">Sign in</a></p>
        </div>
      </div>
    </div>
  );
};

export default Register; 