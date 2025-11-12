import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import EventsPage from "./pages/EventsPage";
import DashboardPage from "./pages/DashboardPage"; // ✅ NEW

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("token") // so it stays logged in after refresh
  );

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            isLoggedIn ? (
              <Navigate to="/dashboard" /> // ✅ redirect to dashboard now
            ) : (
              <LoginPage onLogin={() => setIsLoggedIn(true)} />
            )
          }
        />
        <Route
          path="/dashboard"
          element={isLoggedIn ? <DashboardPage /> : <Navigate to="/" />}
        />
        <Route
          path="/events"
          element={isLoggedIn ? <EventsPage /> : <Navigate to="/" />}
        />
      </Routes>
    </Router>
  );
}

export default App;
