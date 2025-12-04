import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import EventsPage from "./pages/EventsPage";
import JoinLeaveGroupPage from "./pages/JoinLeaveGroupPage";
import CreateGroupPage from "./pages/CreateGroupPage";
import ManageGroupsPage from "./pages/ManageGroupsPage";

function App() {
  const [username, setUsername] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    const storedUsername = localStorage.getItem("username");
    if (token && storedUsername) {
      setIsAuthenticated(true);
      setUsername(storedUsername);
    }
  }, []);

  const handleLogin = (user) => {
    setIsAuthenticated(true);
    setUsername(user);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setUsername(null);
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    sessionStorage.removeItem("user");
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage onLogin={handleLogin} />} />
        
        <Route
          path="/dashboard"
          element={
            isAuthenticated ? (
              <DashboardPage username={username} onLogout={handleLogout} />
            ) : (
              <Navigate to="/" />
            )
          }
        />

        <Route
          path="/events"
          element={
            isAuthenticated ? (
              <EventsPage username={username} />
            ) : (
              <Navigate to="/" />
            )
          }
        />

        <Route
          path="/view_groups"
          element={
            isAuthenticated ? (
              <JoinLeaveGroupPage username={username} />
            ) : (
              <Navigate to="/" />
            )
          }
        />

        <Route
          path="/create_group"
          element={
            isAuthenticated ? (
              <CreateGroupPage username={username} />
            ) : (
              <Navigate to="/" />
            )
          }
        />

        <Route
          path="/manage_groups"
          element={
            isAuthenticated ? (
              <ManageGroupsPage username={username} />
            ) : (
              <Navigate to="/" />
            )
          }
        />
      </Routes>
    </Router>
  );
}

export default App;