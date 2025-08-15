import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const recommendationsService = {
  // Get discover recommendations
  getDiscoverRecommendations: async (token) => {
    const response = await axios.get(`${API_URL}/recommendations/discover`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  },

  // Get user recommendations
  getUserRecommendations: async (token) => {
    const response = await axios.get(`${API_URL}/recommendations/users`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.data;
  }
}; 