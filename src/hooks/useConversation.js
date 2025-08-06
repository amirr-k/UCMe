import { useState, useEffect, useCallback } from 'react';
import { getConversation, sendMessage, markConversationAsRead } from '../services/messageService';

export default function Conversations(conversationId) {
    const [conversation, setConversation] = useState(null);
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const getConversation = useCallback(async () => {
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

    const sendMessage = useCallback(async (content) => {
        if (!conversationId) return;
        if (!content.trim()) return;
        try{
            const sendMessage = await sendMessage(conversationId, content);
            setMessages((prevMessages) => [...prevMessages, sendMessage]);
            return sendMessage;
        }
        catch (error) {
            setError(error.message);
            console.error('Error sending message:', error);
            return null;
        }
    }, [conversationId]);

    const markAsRead = useCallback(async () => {
        if (!conversationId) return;
        try {
            await markConversationAsRead(conversationId);
            setConversation((prevConversation) => ({...prevConversation, unreadCount: 0}));
        }
        catch (error) {
            setError(error.message);
            console.error('Error marking conversation as read:', error);
        }
    }, [conversationId]);

   
}