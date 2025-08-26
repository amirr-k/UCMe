import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const normalize = (value) => {
  if (!value || typeof value !== 'string') return value;
  const key = value.trim().toLowerCase();
  const map = {
    male: 'Male', m: 'Male', men: 'Male', man: 'Male',
    female: 'Female', f: 'Female', women: 'Female', woman: 'Female',
    everyone: 'Everyone', any: 'Everyone', all: 'Everyone'
  };
  return map[key] || value.charAt(0).toUpperCase() + value.slice(1).toLowerCase();
};

export const profileService = {
  getMyProfile: async (token) => {
    const response = await axios.get(`${API_URL}/profile/me`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  },

  updateProfile: async (profileData, token) => {
    const payload = { ...profileData };
    if (payload.gender) payload.gender = normalize(payload.gender);

    const response = await axios.put(`${API_URL}/profile/update`, payload, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  },

  updatePreferences: async (preferencesData, token) => {
    const payload = { ...preferencesData };
    if (payload.genderPref) payload.genderPref = normalize(payload.genderPref);
    const response = await axios.put(`${API_URL}/profile/preferences`, payload, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  },

  viewProfile: async (userId, token) => {
    const response = await axios.get(`${API_URL}/profile/viewProfile/${userId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  },

  uploadImage: async (file, token, isPrimary = true) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('isPrimary', String(isPrimary));
    const response = await axios.post(`${API_URL}/images/upload`, formData, {
      headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  },

  setPrimaryImage: async (imageId, token) => {
    const response = await axios.put(`${API_URL}/images/${imageId}/set-primary`, {}, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  },

  deleteImage: async (imageId, token) => {
    const response = await axios.delete(`${API_URL}/images/${imageId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  }
};
