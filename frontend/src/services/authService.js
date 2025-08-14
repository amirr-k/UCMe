import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const authService = {
  // Request verification code for registration
  requestRegistrationCode: async (email) => {
    const response = await axios.post(`${API_URL}/auth/register/sendVerification`, null, {
      params: { email }
    });
    return response.data;
  },

  // Register new user
  register: async (userData) => {
    const response = await axios.post(`${API_URL}/auth/register`, userData);
    return response.data;
  },

  // Request verification code for login
  requestLoginCode: async (email) => {
    const response = await axios.post(`${API_URL}/auth/login/sendVerification`, null, {
      params: { email }
    });
    return response.data;
  },

  // Login with verification code
  login: async (email, verificationCode) => {
    const response = await axios.post(`${API_URL}/auth/login`, {
      email,
      verificationCode
    });
    return response.data;
  },

  // Resend verification code
  resendVerificationCode: async (email) => {
    const response = await axios.post(`${API_URL}/auth/resendVerification`, null, {
      params: { email }
    });
    return response.data;
  }
}; 