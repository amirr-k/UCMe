import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const interactionsService = {
  // Get user matches
  getMatches: async (token) => {
    const response = await axios.get(`${API_URL}/interactions/matches`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  },

  // Like a profile (swipe right)
  likeProfile: async (targetUserId, token) => {
    const response = await axios.post(`${API_URL}/interactions/like`, null, {
      params: { targetId: targetUserId },
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  },

  // Pass a profile (swipe left)
  passProfile: async (targetUserId, token) => {
    const response = await axios.post(`${API_URL}/interactions/pass`, null, {
      params: { targetId: targetUserId },
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  },

  // Get sent likes
  getSentLikes: async (token) => {
    const response = await axios.get(`${API_URL}/interactions/sentLikes`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  },

  // Get received likes
  getReceivedLikes: async (token) => {
    const response = await axios.get(`${API_URL}/interactions/receivedLikes`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  }
}; 