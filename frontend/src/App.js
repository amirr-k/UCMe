import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/auth/ProtectedRoute';
import Navigation from './components/common/Navigation';
import HomePage from './components/home/HomePage';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import Logout from './components/auth/Logout';
import ConversationsList from './components/messaging/ConversationsList';
import ConversationDetail from './components/messaging/ConversationDetail';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Navigation />
        <Routes>
          <Route path="/" element={<HomePage />} />
          
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/logout" element={<Logout />} />
          
          <Route path="/discover" element={
            <ProtectedRoute>
              <div>Discover/Swipe Page - Coming Soon</div>
            </ProtectedRoute>
          } />
          <Route path="/matches" element={
            <ProtectedRoute>
              <div>Matches Page - Coming Soon</div>
            </ProtectedRoute>
          } />
          <Route path="/profile" element={
            <ProtectedRoute>
              <div>Profile Page - Coming Soon</div>
            </ProtectedRoute>
          } />
          
          <Route path="/messages" element={
            <ProtectedRoute>
              <ConversationsList />
            </ProtectedRoute>
          } />
          <Route path="/messages/:conversationId" element={
            <ProtectedRoute>
              <ConversationDetail />
            </ProtectedRoute>
          } />
          
          <Route path="/settings" element={
            <ProtectedRoute>
              <div>Settings Page - Coming Soon</div>
            </ProtectedRoute>
          } />
          
          <Route path="*" element={<div>Page Not Found</div>} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;