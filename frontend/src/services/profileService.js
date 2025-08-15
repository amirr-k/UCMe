import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const profileService = {
  // Get current user profile
  getCurrentProfile: async (token) => {
    const response = await axios.get(`${API_URL}/profile/me`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  },

  // Update profile
  updateProfile: async (profileData, token) => {
    const response = await axios.put(`${API_URL}/profile/update`, profileData, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  },

  // Update preferences
  updatePreferences: async (preferencesData, token) => {
    const response = await axios.put(`${API_URL}/profile/preferences`, preferencesData, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  },

  // View other user profile
  viewOtherProfile: async (userId, token) => {
    const response = await axios.get(`${API_URL}/profile/viewProfile/${userId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  }
}; 