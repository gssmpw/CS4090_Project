import React from "react";
import { useNavigate } from "react-router-dom";

export default function DashboardPage() {
  const navigate = useNavigate();
  const username = localStorage.getItem("username");

  const handleGoToEvents = () => {
    navigate("/events");
  };

  const handleLogout = () => {
    localStorage.removeItem("username");
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div style={{
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      minHeight: "100vh",
      backgroundColor: "#f8f9fa"
    }}>
      <div style={{
        width: "100%",
        maxWidth: "400px",
        backgroundColor: "white",
        borderRadius: "8px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
        padding: "40px",
        textAlign: "center"
      }}>
        <h2 style={{ marginBottom: "20px" }}>Welcome, {username}!</h2>
        <p style={{ color: "#555", marginBottom: "24px" }}>
          Choose where you'd like to go:
        </p>

        <button
          onClick={handleGoToEvents}
          style={{
            width: "100%",
            padding: "12px",
            backgroundColor: "#007bff",
            color: "white",
            border: "none",
            borderRadius: "4px",
            fontSize: "16px",
            fontWeight: "500",
            marginBottom: "16px",
            cursor: "pointer"
          }}
        >
          View Events
        </button>

        <button
          onClick={handleLogout}
          style={{
            width: "100%",
            padding: "12px",
            backgroundColor: "#dc3545",
            color: "white",
            border: "none",
            borderRadius: "4px",
            fontSize: "16px",
            fontWeight: "500",
            cursor: "pointer"
          }}
        >
          Logout
        </button>
      </div>
    </div>
  );
}
