import { useState, useEffect, useCallback } from 'react';
import { getConversation, sendMessage, markConversationAsRead } from '../services/messageService';

export default function Conversations(conversationId) {
    const [conversation, setConversation] = useState(null);
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchConversation = useCallback(async () => {
        if (!conversationId) return;
        setLoading(true);
        try{
            const data = await getConversation(conversationId);
            setConversation(data);
            setMessages(data.messages || []);
        }
        catch (error) {
            setError(error.message);
            console.error('Error fetching conversation:', error);
        }
        finally {
            setLoading(false);
        }
    }, [conversationId]);

    
    
    
}