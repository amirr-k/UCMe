import React, { useState } from 'react';
import '../../styles/messaging/MessageInput.css';

function MessageInput({ onSendMessage, disabled }) {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!message.trim()) return;
    
    onSendMessage(message);
    setMessage('');
  };