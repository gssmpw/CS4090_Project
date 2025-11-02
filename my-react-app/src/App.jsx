import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import EventsPage from "./pages/EventsPage";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            isLoggedIn ? <Navigate to="/events" /> : <LoginPage onLogin={() => setIsLoggedIn(true)} />
          }
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
