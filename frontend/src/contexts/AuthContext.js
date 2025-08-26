import React, { createContext, useContext, useState, useEffect } from 'react';
import { profileService } from '../services/profileService';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('token'));

  // Check if user is authenticated
  const isAuthenticated = !!token && !!user;

  const fetchAndSetUser = async (authToken, fallbackUser) => {
    try {
      const fullProfile = await profileService.getMyProfile(authToken);
      setUser(fullProfile);
      localStorage.setItem('user', JSON.stringify(fullProfile));
    } catch (error) {
      console.error('Failed to fetch user profile:', error);
      if (fallbackUser) {
        setUser(fallbackUser);
        localStorage.setItem('user', JSON.stringify(fallbackUser));
      }
    }
  };

  // Login function
  const login = (userData, authToken) => {
    setToken(authToken);
    localStorage.setItem('token', authToken);
    // Attempt to fetch full profile; fall back to provided userData
    fetchAndSetUser(authToken, userData);
  };

  // Logout function
  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  // Check authentication status on app load
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const storedToken = localStorage.getItem('token');
        const storedUser = localStorage.getItem('user');
        
        if (storedToken) {
          setToken(storedToken);
          if (storedUser) {
            const parsed = JSON.parse(storedUser);
            setUser(parsed);
            // If stored user lacks essential fields, refresh from API
            if (!parsed?.id || !parsed?.name) {
              await fetchAndSetUser(storedToken, parsed);
            }
          } else {
            await fetchAndSetUser(storedToken, null);
          }
        }
      } catch (error) {
        console.error('Auth check failed:', error);
        logout();
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const value = {
    user,
    token,
    isAuthenticated,
    loading,
    login,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 