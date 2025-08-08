import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ConversationsList from './components/messaging/ConversationsList';
import ConversationDetail from './components/messaging/ConversationDetail';

function App() {
  return (
    <Router>
      <Routes>
        {
        <Route path="/" element={<div>////// PLACEHOLDER RN</div>} />
        {}
        <Route path="/messages" element={<ConversationsList />} />
        <Route path="/messages/:conversationId" element={<ConversationDetail />} />
        
        {}
      </Routes>
    </Router>
  );
}

export default App;