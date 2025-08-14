import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { authService } from '../../services/authService';
import './Login.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [verificationCode, setVerificationCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [step, setStep] = useState('email'); // 'email' | 'verify'
  const [countdown, setCountdown] = useState(0);

  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || '/';

  // Prefill email if passed from previous flow (e.g., after registration)
  useEffect(() => {
    if (location.state?.email) {
      setEmail(location.state.email);
    }
  }, [location.state]);

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
      await authService.requestLoginCode(email);
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

  const handleVerifyCode = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await authService.login(email, verificationCode);
      login({ email }, response.accessToken);
      navigate(from, { replace: true });
    } catch (err) {
      setError(err?.response?.data?.detail || 'Invalid verification code. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    setStep('email');
    setVerificationCode('');
    setError('');
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>Welcome to UCMe</h1>
        <p className="subtitle">Connect with UC students</p>

        {error && <div className="error-message">{error}</div>}

        {step === 'email' ? (
          <form onSubmit={handleRequestCode} className="login-form">
            <div className="form-group">
              <label htmlFor="email">UC Email</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your.email@uc.edu"
                required
                className="form-input"
                disabled={loading}
              />
            </div>

            <button type="submit" disabled={loading} className="login-button">
              {loading ? 'Sending Code...' : 'Get Verification Code'}
            </button>
          </form>
        ) : (
          <form onSubmit={handleVerifyCode} className="login-form">
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
                  onClick={handleBack}
                  className="back-button"
                  disabled={loading}
                >
                  Use different email
                </button>
              </div>
            </div>

            <button type="submit" disabled={loading || verificationCode.length !== 6} className="login-button">
              {loading ? 'Verifying...' : 'Sign In'}
            </button>
          </form>
        )}

        <div className="login-footer">
          <p>
            Don't have an account? <a href="/register">Sign up</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login; 