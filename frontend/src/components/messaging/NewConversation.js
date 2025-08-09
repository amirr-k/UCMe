import React from 'react';
import { useNavigate } from 'react-router-dom';
import { createConversation } from '../../services/messageService';
import '../../styles/messaging/NewConversation.css';

function NewConversation({ userId, userName, userImage, onConversationCreated }) {
    const navigate = useNavigate();
    const [creating, setCreating] = React.useState(false);
    const [error, setError] = React.useState(null);
    
    const handleStartConversation = async () => {
        setCreating(true);
        setError(null);

        try {
            const conversation = await createConversation(userId);
            if (onConversationCreated) {
                onConversationCreated(conversation);
            } else {
                navigate(`/messages/${conversation.id}`);
            }
        } catch (error) {
            setError(error);
            console.error('Error starting conversation:', error);
        } finally {
            setCreating(false);
        }
    };
    
    return (
        <div className="new-conversation">
            {error && (
                <div className="error-message">
                    Failed to start conversation. Please try again.
                </div>
            )}
            <button 
                className="message-button"
                onClick={handleStartConversation}
                disabled={creating}
            >
                {creating ? 'Starting chat...' : 'Message'}
            </button>
        </div>
    );
}

export default NewConversation;