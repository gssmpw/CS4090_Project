import React from "react";
import { useNavigate } from "react-router-dom";

export default function NotificationsPage() {
  const navigate = useNavigate();

  // Get user info from sessionStorage
  const user = JSON.parse(sessionStorage.getItem("user") || "{}");

  const handleLogout = () => {
    sessionStorage.removeItem("user");
    localStorage.removeItem("username");
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
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
      {/* Page Title */}
      <h1 style={{ margin: 0, fontSize: "24px" }}>Notifications</h1>

      {/* Right side controls */}
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
  );
}
