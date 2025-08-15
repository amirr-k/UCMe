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

  // Swipe right (like)
  swipeRight: async (targetUserId, token) => {
    const response = await axios.post(`${API_URL}/interactions/swipe`, {
      targetUserId,
      swipeType: 'right'
    }, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  },

  // Swipe left (pass)
  swipeLeft: async (targetUserId, token) => {
    const response = await axios.post(`${API_URL}/interactions/swipe`, {
      targetUserId,
      swipeType: 'left'
    }, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  },

  // Get swipe history
  getSwipeHistory: async (token) => {
    const response = await axios.get(`${API_URL}/interactions/swipes`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  }
}; 