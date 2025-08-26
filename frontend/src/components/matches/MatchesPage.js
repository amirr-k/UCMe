import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";
import { interactionsService } from "../../services/interactionsService";
import { createConversation } from "../../services/messageService";
import "./MatchesPage.css";

export default function MatchesPage() {
  const { token } = useAuth();
  const navigate = useNavigate();
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const data = await interactionsService.getMatches(token);
        setMatches(data);
      } catch (err) {
        console.error("load matches error", err);
        setError("Couldn't load matches");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [token]);

  const messageClick = async (id) => {
    try {
      const convo = await createConversation(id);
      navigate(`/messages/${convo.id}`);
    } catch {
      navigate("/messages");
    }
  };

  if (loading) {
    return (
      <div className="matches-container">
        <div className="loading-spinner">
          <div className="spinner" />
          <p>Loading matches...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="matches-container">
        <div className="error-message">
          <p>{error}</p>
          <button onClick={() => window.location.reload()} className="retry-button">
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!matches.length) {
    return (
      <div className="matches-container">
        <div className="no-matches">
          <div className="no-matches-icon">💔</div>
          <h2>No Matches</h2>
          <p>Try Discover to start swiping</p>
          <button onClick={() => navigate("/discover")} className="discover-button">
            Go to Discover
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="matches-container">
      <div className="matches-header">
        <h1>Your Matches</h1>
        <p>{matches.length} total</p>
      </div>

      <div className="matches-grid">
        {matches.map((m) => {
          const img = m.user.images?.find((i) => i.isPrimary) || m.user.images?.[0];
          const src = img ? (img.imageUrl.startsWith("http") ? img.imageUrl : `http://localhost:8000/${img.imageUrl}`) : null;

          return (
            <div key={m.id} className="match-card">
              <div className="match-image-container">
                {src ? (
                  <img src={src} alt={m.user.name} className="match-image" />
                ) : (
                  <div className="match-image-placeholder">
                    <span>{m.user.name?.charAt(0) || "U"}</span>
                  </div>
                )}
              </div>

              <div className="match-info">
                <h3>
                  {m.user.name || "Anonymous"}, {m.user.age || "N/A"}
                </h3>
                <p className="match-college">{m.user.college || "N/A"}</p>
                <p className="match-major">{m.user.major || "N/A"}</p>

                {m.user.interests?.length > 0 && (
                  <div className="match-interests">
                    {m.user.interests.slice(0, 3).map((int, i) => (
                      <span key={i} className="interest-tag">
                        {int}
                      </span>
                    ))}
                    {m.user.interests.length > 3 && (
                      <span className="interest-more">+{m.user.interests.length - 3} more</span>
                    )}
                  </div>
                )}

                <div className="match-actions">
                  <button onClick={() => messageClick(m.user.id)} className="action-button primary">
                    Message
                  </button>
                  <button onClick={() => navigate(`/profile/${m.user.id}`)} className="action-button secondary">
                    View
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}