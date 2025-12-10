import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Get user info from sessionStorage
  const user = JSON.parse(sessionStorage.getItem("user") || "{}");
  const username = user.username;

  const handleLogout = () => {
    sessionStorage.removeItem("user");
    localStorage.removeItem("username");
    localStorage.removeItem("token");
    navigate("/");
  };

  useEffect(() => {
    if (!username) {
      navigate("/");
      return;
    }
    fetchNotifications();
  }, [username]);

  const fetchNotifications = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`http://localhost:8002/notifications/${username}`);
      if (response.ok) {
        const data = await response.json();
        setNotifications(data);
      } else {
        setError("Failed to load notifications");
      }
    } catch (err) {
      console.error("Error fetching notifications:", err);
      setError("Failed to connect to server. Make sure backend is running on http://localhost:8002");
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString("en-US", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  if (loading) {
    return (
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh" }}>
        <div style={{ fontSize: "18px", color: "#666" }}>Loading notifications...</div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#f8f9fa" }}>
      {/* Header */}
      <div
        style={{
          backgroundColor: "white",
          borderBottom: "1px solid #ddd",
          padding: "16px 24px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <h1 style={{ margin: 0, fontSize: "24px" }}>Notifications</h1>
        <div style={{ display: "flex", gap: "12px", alignItems: "center" }}>
          <span style={{ color: "#666", fontSize: "14px" }}>
            Welcome, {user.Fname} {user.Lname}
          </span>
          <button
            onClick={() => navigate("/dashboard")}
            style={{
              padding: "8px 16px",
              backgroundColor: "#6c757d",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
              fontSize: "14px",
            }}
          >
            Dashboard
          </button>
          <button
            onClick={handleLogout}
            style={{
              padding: "8px 16px",
              backgroundColor: "#dc3545",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
              fontSize: "14px",
            }}
          >
            Logout
          </button>
        </div>
      </div>

      {/* Notifications Content */}
      <div style={{ padding: "24px", maxWidth: "1200px", margin: "0 auto" }}>
        {error && (
          <div
            style={{
              padding: "16px",
              marginBottom: "24px",
              backgroundColor: "#f8d7da",
              color: "#721c24",
              borderRadius: "8px",
              border: "1px solid #f5c6cb",
            }}
          >
            {error}
          </div>
        )}

        {notifications.length === 0 ? (
          <div
            style={{
              backgroundColor: "white",
              borderRadius: "8px",
              padding: "48px",
              textAlign: "center",
              boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
            }}
          >
            <div style={{ fontSize: "48px", marginBottom: "16px" }}>🔔</div>
            <h2 style={{ marginTop: 0, marginBottom: "8px", color: "#666" }}>No Notifications</h2>
            <p style={{ color: "#999", margin: 0 }}>You're all caught up!</p>
          </div>
        ) : (
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(350px, 1fr))", gap: "20px" }}>
            {notifications.map((note) => (
              <div
                key={note.notificationID || `${note.username}-${note.eventID}-${note.notificationTimestamp}`}
                style={{
                  backgroundColor: "white",
                  borderRadius: "8px",
                  padding: "20px",
                  boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
                  border: "1px solid #e0e0e0",
                }}
              >
                <div style={{ display: "flex", alignItems: "center", marginBottom: "12px" }}>
                  <div
                    style={{
                      width: "48px",
                      height: "48px",
                      backgroundColor: "#ffc107",
                      borderRadius: "8px",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      marginRight: "12px",
                      fontSize: "24px",
                    }}
                  >
                    🔔
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: "12px", color: "#666", marginBottom: "4px" }}>
                      {formatDate(note.notificationTimestamp)}
                    </div>
                    <div style={{ fontSize: "14px", fontWeight: "600", color: "#333" }}>
                      Event Date: {formatDate(note.eventDate)}
                    </div>
                  </div>
                </div>

                <div
                  style={{
                    fontSize: "16px",
                    fontWeight: "500",
                    color: "#333",
                    marginBottom: "8px",
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    display: "-webkit-box",
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: "vertical",
                  }}
                >
                  {note.description || "No description"}
                </div>

                <div style={{ fontSize: "13px", color: note.isRead ? "#28a745" : "#dc3545", marginTop: "12px", fontWeight: "500" }}>
                  {note.isRead ? "Read" : "Unread"}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
