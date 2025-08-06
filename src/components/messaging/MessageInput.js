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

  return (
    <form className="message-input-container" onSubmit={handleSubmit}>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type a message..."
        disabled={disabled}
        className="message-input"
      />
      <button 
        type="submit"
        disabled={disabled || !message.trim()}
        className="send-button">Send
      </button>
    </form>
  );
}

export default MessageInput;