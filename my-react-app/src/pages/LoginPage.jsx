import React, { useState } from "react";
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from "react-router-dom";

function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await fetch('http://localhost:8001/login', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
      });
      
      if (response.ok) {
        const userData = await response.json();
        
        // Store user data in sessionStorage
        sessionStorage.setItem('user', JSON.stringify(userData));
        
        // Navigate to dashboard
        navigate('/dashboard');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Invalid username or password');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError('Failed to connect to server. Make sure the backend is running on http://localhost:8001');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh", backgroundColor: "#f8f9fa" }}>
      <div style={{ width: "100%", maxWidth: "400px", backgroundColor: "white", borderRadius: "8px", boxShadow: "0 2px 8px rgba(0,0,0,0.1)", padding: "40px" }}>
        <h3 style={{ textAlign: "center", marginBottom: "24px", fontSize: "24px" }}>Login</h3>
        
        {error && (
          <div style={{ padding: "12px", marginBottom: "20px", backgroundColor: "#f8d7da", color: "#721c24", borderRadius: "4px", border: "1px solid #f5c6cb", fontSize: "14px" }}>
            {error}
          </div>
        )}

        <div>
          <div style={{ marginBottom: "20px" }}>
            <label style={{ display: "block", marginBottom: "8px", fontWeight: "500", fontSize: "14px" }}>Username</label>
            <input 
              type="text" 
              value={username} 
              onChange={(e) => setUsername(e.target.value)} 
              onKeyPress={(e) => e.key === 'Enter' && handleSubmit(e)}
              placeholder="Enter username" 
              disabled={loading} 
              style={{ width: "100%", padding: "10px", border: "1px solid #ddd", borderRadius: "4px", fontSize: "14px", boxSizing: "border-box" }} 
            />
          </div>

          <div style={{ marginBottom: "24px" }}>
            <label style={{ display: "block", marginBottom: "8px", fontWeight: "500", fontSize: "14px" }}>Password</label>
            <input 
              type="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              onKeyPress={(e) => e.key === 'Enter' && handleSubmit(e)}
              placeholder="Enter password" 
              disabled={loading} 
              style={{ width: "100%", padding: "10px", border: "1px solid #ddd", borderRadius: "4px", fontSize: "14px", boxSizing: "border-box" }} 
            />
          </div>

          <button 
            onClick={handleSubmit}
            disabled={loading} 
            style={{ 
              width: "100%", 
              padding: "12px", 
              backgroundColor: loading ? "#6c757d" : "#007bff", 
              color: "white", 
              border: "none", 
              borderRadius: "4px", 
              fontSize: "16px", 
              fontWeight: "500", 
              cursor: loading ? "not-allowed" : "pointer" 
            }}
          >
            {loading ? "Logging in..." : "Sign In"}
          </button>
        </div>

        <div style={{ marginTop: "24px", padding: "16px", backgroundColor: "#f8f9fa", borderRadius: "4px", fontSize: "13px", color: "#666" }}>
          <p style={{ margin: "0 0 8px 0", fontWeight: "600", color: "#333" }}>Test Accounts:</p>
          <p style={{ margin: "4px 0" }}><strong>jsmith</strong> / Pass123!</p>
          <p style={{ margin: "4px 0" }}><strong>adavis</strong> / SecurePass456</p>
          <p style={{ margin: "4px 0" }}><strong>mjohnson</strong> / MyPassword789</p>
        </div>
      </div>
    </div>
  );
}

// Protected Route Component
function ProtectedRoute({ children }) {
  const user = sessionStorage.getItem('user');
  
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              {/* This will be replaced with your actual Dashboard component */}
              <div style={{ padding: "20px" }}>
                <h1>Dashboard Page</h1>
                <p>Import your Dashboard.jsx component here</p>
                <p>User data is available in sessionStorage</p>
              </div>
            </ProtectedRoute>
          } 
        />
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}