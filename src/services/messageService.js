import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const getAuthHeader = () => {
    const token = localStorage.getItem('token');
    return { Authorization: `Bearer ${token}` };
  };


  export const getConversations = async (skip = 0, limit = 20) => {
    try {
      const response = await axios.get(`${API_URL}/messages/conversations?skip=${skip}&limit=${limit}`, {
        headers: getAuthHeader()
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching conversations:', error);
      throw error;
    }
  };

  export const getConversation = async (conversationId) => {
    try {
      const response = await axios.get(`${API_URL}/messages/conversations/${conversationId}`, {
        headers: getAuthHeader()
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching conversation:', error);
      throw error;
    }
  };

  export const markAsRead = async (conversationId) => {
    try {
      const response = await axios.put(
        `${API_URL}/messages/conversations/${conversationId}/read`,
        {},
        { headers: getAuthHeader() }
      );
      return response.data;
    } catch (error) {
      console.error('Error marking conversation as read:', error);
      throw error;
    }
  };

  export const sendMessage = async (conversationId, content) => {
    try {
      const response = await axios.post(
        `${API_URL}/messages/conversations/${conversationId}/messages`,
        { content },
        { headers: getAuthHeader() }
      );
      return response.data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  };

  