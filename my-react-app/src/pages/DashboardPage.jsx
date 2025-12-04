import React from "react";
import { useNavigate } from "react-router-dom";

export default function DashboardPage({ username, onLogout }) {
  const navigate = useNavigate();

  const handleGoToEvents = () => {
    navigate("/events");
  };

  const handleGoToGroups = () => {
    navigate("/view_groups");
  };

  const handleGoToNotifications = () => {
    navigate("/notifications");
  };

  const handleLogout = () => {
    onLogout();
    navigate("/");
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        background: "linear-gradient(to right, #e3f2fd, #ffffff)",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "450px",
          backgroundColor: "white",
          borderRadius: "12px",
          boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
          padding: "40px",
          textAlign: "center",
        }}
      >
        <div style={{ marginBottom: "30px" }}>
          <h1 style={{ marginBottom: "10px", color: "#007bff" }}>
            Welcome back, {username}!
          </h1>
        </div>

        {/* Buttons */}
        <div>
          <button
            onClick={handleGoToEvents}
            style={buttonStyle("#007bff", "#0056b3")}
          >
            View Events
          </button>

          <button
            onClick={handleGoToGroups}
            style={buttonStyle("#17a2b8", "#11707f")}
          >
            View Groups
          </button>

          <button
            onClick={handleGoToNotifications}
            style={buttonStyle("#17a2be", "#11707f")}
          >
            View Notifications
          </button>


          <button
            onClick={handleLogout}
            style={buttonStyle("#dc3545", "#a71d2a")}
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  );
}

// Helper for consistent button styles
function buttonStyle(baseColor, hoverColor) {
  return {
    width: "100%",
    padding: "12px",
    backgroundColor: baseColor,
    color: "white",
    border: "none",
    borderRadius: "6px",
    fontSize: "16px",
    fontWeight: "500",
    marginBottom: "16px",
    cursor: "pointer",
    transition: "0.2s ease",
    ...(hoverColor && {
      onMouseOver: (e) => (e.target.style.backgroundColor = hoverColor),
      onMouseOut: (e) => (e.target.style.backgroundColor = baseColor),
    }),
  };
}
