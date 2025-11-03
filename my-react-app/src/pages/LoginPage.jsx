import React, { useState } from "react";

export default function LoginPage({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
      });
      
      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('username', data.username);
        localStorage.setItem('token', data.token);
        onLogin();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Invalid username or password');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError('Failed to connect to server. Make sure the backend is running on http://localhost:8000');
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

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: "20px" }}>
            <label style={{ display: "block", marginBottom: "8px", fontWeight: "500", fontSize: "14px" }}>Username</label>
            <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Enter username" required disabled={loading} style={{ width: "100%", padding: "10px", border: "1px solid #ddd", borderRadius: "4px", fontSize: "14px", boxSizing: "border-box" }} />
          </div>

          <div style={{ marginBottom: "24px" }}>
            <label style={{ display: "block", marginBottom: "8px", fontWeight: "500", fontSize: "14px" }}>Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Enter password" required disabled={loading} style={{ width: "100%", padding: "10px", border: "1px solid #ddd", borderRadius: "4px", fontSize: "14px", boxSizing: "border-box" }} />
          </div>

          <button type="submit" disabled={loading} style={{ width: "100%", padding: "12px", backgroundColor: loading ? "#6c757d" : "#007bff", color: "white", border: "none", borderRadius: "4px", fontSize: "16px", fontWeight: "500", cursor: loading ? "not-allowed" : "pointer" }}>
            {loading ? "Logging in..." : "Sign In"}
          </button>
        </form>

        <div style={{ marginTop: "24px", padding: "16px", backgroundColor: "#f8f9fa", borderRadius: "4px", fontSize: "13px", color: "#666" }}>
          <p style={{ margin: "0 0 8px 0", fontWeight: "600", color: "#333" }}>Test Accounts:</p>
          <p style={{ margin: "4px 0" }}><strong>john</strong> / password123</p>
          <p style={{ margin: "4px 0" }}><strong>alice</strong> / pass456</p>
          <p style={{ margin: "4px 0" }}><strong>bob</strong> / test789</p>
        </div>
      </div>
    </div>
  );
}