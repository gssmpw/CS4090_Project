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

  const handleManageGroups = () => {
    navigate("/manage_groups");
  };

  const handleCreateGroup = () => {
    navigate("/create_group");
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
            onMouseOver={(e) => (e.target.style.backgroundColor = "#0056b3")}
            onMouseOut={(e) => (e.target.style.backgroundColor = "#007bff")}
          >
            View Events
          </button>

          <button
            onClick={handleGoToGroups}
            style={buttonStyle("#17a2b8", "#11707f")}
            onMouseOver={(e) => (e.target.style.backgroundColor = "#11707f")}
            onMouseOut={(e) => (e.target.style.backgroundColor = "#17a2b8")}
          >
            View Groups
          </button>

          <button
            onClick={handleManageGroups}
            style={buttonStyle("#28a745", "#1e7e34")}
            onMouseOver={(e) => (e.target.style.backgroundColor = "#1e7e34")}
            onMouseOut={(e) => (e.target.style.backgroundColor = "#28a745")}
          >
            Manage Groups
          </button>

          <button
            onClick={handleCreateGroup}
            style={buttonStyle("#6f42c1", "#5a32a3")}
            onMouseOver={(e) => (e.target.style.backgroundColor = "#5a32a3")}
            onMouseOut={(e) => (e.target.style.backgroundColor = "#6f42c1")}
          >
            Create Group
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
            onMouseOver={(e) => (e.target.style.backgroundColor = "#a71d2a")}
            onMouseOut={(e) => (e.target.style.backgroundColor = "#dc3545")}
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
    transition: "background-color 0.2s ease",
  };
}