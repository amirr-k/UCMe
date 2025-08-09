import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ConversationsList from './components/messaging/ConversationsList';
import ConversationDetail from './components/messaging/ConversationDetail';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<div>Welcome to UCMe - Dating App for UC Students</div>} />
        
        <Route path="/login" element={<div>Login Page - Coming Soon</div>} />
        <Route path="/register" element={<div>Register Page - Coming Soon</div>} />
        
        <Route path="/discover" element={<div>Discover/Swipe Page - Coming Soon</div>} />
        <Route path="/matches" element={<div>Matches Page - Coming Soon</div>} />
        <Route path="/profile" element={<div>Profile Page - Coming Soon</div>} />
        
        <Route path="/messages" element={<ConversationsList />} />
        <Route path="/messages/:conversationId" element={<ConversationDetail />} />
        
        <Route path="/settings" element={<div>Settings Page - Coming Soon</div>} />
        
        <Route path="*" element={<div>Page Not Found</div>} />
      </Routes>
    </Router>
  );
}

export default App;