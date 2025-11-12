import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import EventsPage from "./pages/EventsPage";
import DashboardPage from "./pages/DashboardPage";
import JoinLeaveGroupPage from "./pages/JoinLeaveGroupPage";

function App() {
  // Load token and username from localStorage on startup
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("token"));
  const [username, setUsername] = useState(localStorage.getItem("username") || "");

  // Keep localStorage in sync when username changes
  useEffect(() => {
    if (username) {
      localStorage.setItem("username", username);
    }
  }, [username]);

  // Handle login from LoginPage
  const handleLogin = (username) => {
    setIsLoggedIn(true);
    setUsername(username);
  };

  // Handle logout (shared by all pages)
  const handleLogout = () => {
    localStorage.removeItem("username");
    localStorage.removeItem("token");
    setIsLoggedIn(false);
    setUsername("");
  };

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            isLoggedIn ? (
              <Navigate to="/dashboard" />
            ) : (
              <LoginPage onLogin={handleLogin} />
            )
          }
        />
        <Route
          path="/dashboard"
          element={
            isLoggedIn ? (
              <DashboardPage username={username} onLogout={handleLogout} />
            ) : (
              <Navigate to="/" />
            )
          }
        />
        <Route
          path="/events"
          element={
            isLoggedIn ? (
              <EventsPage username={username} onLogout={handleLogout} />
            ) : (
              <Navigate to="/" />
            )
          }
        />
        <Route
          path="/view_groups"
          element={isLoggedIn ? <JoinLeaveGroupPage /> : <Navigate to="/" />}/>
      </Routes>
    </Router>
  );
}

export default App;