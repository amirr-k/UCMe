function ConversationsList() {
    const [conversations, setConversations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchConversations = async () => {
          setLoading(true);
          try {
            const data = await getConversations();
            setConversations(data);
            setError(null);
          }
          catch (err) {
            setError('Failed to load conversations');
            console.error('Error loading conversations:', err);
          } 
          finally {
            setLoading(false);
          }
        };
    fetchConversations();

    const intervalId = setInterval(fetchConversations, 30000);

    return () => clearInterval (intervalId);
    }, []);

    if (loading) return <div className = "loading">Loading Conversations...</div>
    if (error) return <div className="error">{error}</div>