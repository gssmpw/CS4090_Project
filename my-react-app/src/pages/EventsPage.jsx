import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function EventsPage({ username }) {
  const [events, setEvents] = useState([]);
  const [rsvpStatus, setRsvpStatus] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [rsvpLoading, setRsvpLoading] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    fetchUserEvents();
  }, [username]);

  const fetchUserEvents = async () => {
    setLoading(true);
    setError("");

    try {
      // Fetch user's events
      const eventsResponse = await fetch(`http://localhost:8002/events/user/${username}`);
      
      if (eventsResponse.ok) {
        const eventsData = await eventsResponse.json();
        setEvents(eventsData);
        
        // Fetch RSVP status for all events
        await fetchRSVPStatuses(eventsData);
      } else {
        const errorData = await eventsResponse.json();
        setError(errorData.detail || 'Failed to load events');
      }
    } catch (err) {
      console.error('Fetch events error:', err);
      setError('Failed to connect to server. Make sure the Events Service is running.');
    } finally {
      setLoading(false);
    }
  };

  const fetchRSVPStatuses = async (eventsList) => {
    try {
      const statuses = {};
      for (const event of eventsList) {
        const response = await fetch(`http://localhost:8002/rsvp/${event.eventID}/${username}`);
        if (response.ok) {
          const data = await response.json();
          statuses[event.eventID] = data.isRSVPed;
        } else {
          statuses[event.eventID] = false;
        }
      }
      setRsvpStatus(statuses);
    } catch (err) {
      console.error('Fetch RSVP status error:', err);
    }
  };

  const handleRSVP = async (eventId) => {
    setRsvpLoading({ ...rsvpLoading, [eventId]: true });

    try {
      const response = await fetch(`http://localhost:8002/rsvp/${eventId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username })
      });

      if (response.ok) {
        setRsvpStatus({ ...rsvpStatus, [eventId]: true });
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to RSVP');
      }
    } catch (err) {
      console.error('RSVP error:', err);
      setError('Failed to connect to server.');
    } finally {
      setRsvpLoading({ ...rsvpLoading, [eventId]: false });
    }
  };

  const handleUnRSVP = async (eventId) => {
    setRsvpLoading({ ...rsvpLoading, [eventId]: true });

    try {
      const response = await fetch(`http://localhost:8002/rsvp/${eventId}/${username}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        setRsvpStatus({ ...rsvpStatus, [eventId]: false });
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to un-RSVP');
      }
    } catch (err) {
      console.error('Un-RSVP error:', err);
      setError('Failed to connect to server.');
    } finally {
      setRsvpLoading({ ...rsvpLoading, [eventId]: false });
    }
  };

  const handleBack = () => {
    navigate('/dashboard');
  };

  const formatDateTime = (dateString) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return dateString;
    }
  };

  return (
    <div style={{ 
      minHeight: "100vh", 
      background: "linear-gradient(to right, #e3f2fd, #ffffff)",
      padding: "40px 20px"
    }}>
      <div style={{ 
        maxWidth: "800px", 
        margin: "0 auto",
        backgroundColor: "white", 
        borderRadius: "12px", 
        boxShadow: "0 4px 12px rgba(0,0,0,0.1)", 
        padding: "40px" 
      }}>
        <div style={{ marginBottom: "30px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <h2 style={{ margin: "0 0 8px 0", color: "#007bff", fontSize: "28px" }}>
              My Events
            </h2>
            <p style={{ margin: 0, color: "#666", fontSize: "14px" }}>
              Events from all your groups
            </p>
          </div>
          <button
            onClick={handleBack}
            style={{
              padding: "10px 20px",
              backgroundColor: "white",
              color: "#007bff",
              border: "2px solid #007bff",
              borderRadius: "6px",
              fontSize: "14px",
              fontWeight: "600",
              cursor: "pointer"
            }}
          >
            ← Back
          </button>
        </div>

        {error && (
          <div style={{ 
            padding: "12px", 
            marginBottom: "20px", 
            backgroundColor: "#f8d7da", 
            color: "#721c24", 
            borderRadius: "6px", 
            border: "1px solid #f5c6cb", 
            fontSize: "14px" 
          }}>
            {error}
          </div>
        )}

        {loading ? (
          <div style={{ textAlign: "center", padding: "40px", color: "#666" }}>
            <div style={{ fontSize: "18px" }}>Loading events...</div>
          </div>
        ) : events.length === 0 ? (
          <div style={{ 
            textAlign: "center", 
            padding: "60px 20px",
            backgroundColor: "#f8f9fa",
            borderRadius: "8px"
          }}>
            <div style={{ fontSize: "48px", marginBottom: "16px" }}>📅</div>
            <h3 style={{ margin: "0 0 12px 0", color: "#333" }}>
              No Events Yet
            </h3>
            <p style={{ margin: 0, color: "#666", fontSize: "14px" }}>
              You don't have any events yet. Join some groups to see their events!
            </p>
          </div>
        ) : (
          <div>
            <div style={{ 
              marginBottom: "20px",
              paddingBottom: "12px",
              borderBottom: "2px solid #e9ecef"
            }}>
              <div style={{ color: "#666", fontSize: "14px" }}>
                {events.length} {events.length === 1 ? 'event' : 'events'} found
              </div>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
              {events.map((event) => {
                const isRSVPed = rsvpStatus[event.eventID] || false;
                const isLoading = rsvpLoading[event.eventID] || false;

                return (
                  <div
                    key={event.eventID}
                    style={{
                      padding: "20px",
                      border: `2px solid ${isRSVPed ? '#28a745' : '#e9ecef'}`,
                      borderRadius: "8px",
                      backgroundColor: isRSVPed ? '#f8fff9' : 'white',
                      transition: "all 0.2s"
                    }}
                  >
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start" }}>
                      <div style={{ flex: 1 }}>
                        <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "8px" }}>
                          <h3 style={{ 
                            margin: 0, 
                            color: "#007bff", 
                            fontSize: "18px",
                            fontWeight: "600"
                          }}>
                            {event.description}
                          </h3>
                          {isRSVPed && (
                            <span style={{
                              padding: "4px 8px",
                              backgroundColor: "#28a745",
                              color: "white",
                              borderRadius: "4px",
                              fontSize: "11px",
                              fontWeight: "600"
                            }}>
                              ✓ RSVP'D
                            </span>
                          )}
                        </div>
                        <div style={{ 
                          margin: "8px 0", 
                          color: "#666", 
                          fontSize: "14px"
                        }}>
                          📅 {formatDateTime(event.date)}
                        </div>
                      </div>

                      <button
                        onClick={() => isRSVPed ? handleUnRSVP(event.eventID) : handleRSVP(event.eventID)}
                        disabled={isLoading}
                        style={{
                          padding: "10px 20px",
                          backgroundColor: isLoading ? "#6c757d" : (isRSVPed ? "#dc3545" : "#28a745"),
                          color: "white",
                          border: "none",
                          borderRadius: "6px",
                          fontSize: "14px",
                          fontWeight: "600",
                          cursor: isLoading ? "not-allowed" : "pointer",
                          whiteSpace: "nowrap",
                          minWidth: "100px"
                        }}
                      >
                        {isLoading ? "..." : (isRSVPed ? "Un-RSVP" : "RSVP")}
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}