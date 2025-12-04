import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function LoginPage({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true); // Toggle between login and register
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  const resetForm = () => {
    setUsername("");
    setPassword("");
    setFirstName("");
    setLastName("");
    setError("");
    setSuccess("");
  };

  const handleLogin = async (e) => {
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
        
        // Store token and username in localStorage for App.jsx compatibility
        localStorage.setItem('token', 'logged-in');
        localStorage.setItem('username', userData.username);
        
        // Call the onLogin prop passed from App.jsx
        onLogin(userData.username);
        
        // Navigate to dashboard page
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

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const response = await fetch('http://localhost:8001/register', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          username, 
          password,
          Fname: firstName,
          Lname: lastName
        })
      });
      
      if (response.ok) {
        const userData = await response.json();
        setSuccess('Account created successfully! You can now login.');
        
        // Reset form and switch to login after 2 seconds
        setTimeout(() => {
          resetForm();
          setIsLogin(true);
        }, 2000);
      } else {
        const errorData = await response.json();
        if (response.status === 409) {
          setError('Username already exists. Please choose a different username.');
        } else {
          setError(errorData.detail || 'Registration failed. Please try again.');
        }
      }
    } catch (err) {
      console.error('Registration error:', err);
      setError('Failed to connect to server. Make sure the backend is running on http://localhost:8001');
    } finally {
      setLoading(false);
    }
  };

  const toggleMode = () => {
    resetForm();
    setIsLogin(!isLogin);
  };

  return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "100vh", backgroundColor: "#f8f9fa" }}>
      <div style={{ width: "100%", maxWidth: "400px", backgroundColor: "white", borderRadius: "8px", boxShadow: "0 2px 8px rgba(0,0,0,0.1)", padding: "40px" }}>
        <h3 style={{ textAlign: "center", marginBottom: "24px", fontSize: "24px" }}>
          {isLogin ? "Login" : "Create Account"}
        </h3>
        
        {error && (
          <div style={{ padding: "12px", marginBottom: "20px", backgroundColor: "#f8d7da", color: "#721c24", borderRadius: "4px", border: "1px solid #f5c6cb", fontSize: "14px" }}>
            {error}
          </div>
        )}

        {success && (
          <div style={{ padding: "12px", marginBottom: "20px", backgroundColor: "#d4edda", color: "#155724", borderRadius: "4px", border: "1px solid #c3e6cb", fontSize: "14px" }}>
            {success}
          </div>
        )}

        <form onSubmit={isLogin ? handleLogin : handleRegister}>
          {!isLogin && (
            <>
              <div style={{ marginBottom: "20px" }}>
                <label style={{ display: "block", marginBottom: "8px", fontWeight: "500", fontSize: "14px" }}>First Name</label>
                <input 
                  type="text" 
                  value={firstName} 
                  onChange={(e) => setFirstName(e.target.value)} 
                  placeholder="Enter first name" 
                  required
                  disabled={loading} 
                  style={{ width: "100%", padding: "10px", border: "1px solid #ddd", borderRadius: "4px", fontSize: "14px", boxSizing: "border-box" }} 
                />
              </div>

              <div style={{ marginBottom: "20px" }}>
                <label style={{ display: "block", marginBottom: "8px", fontWeight: "500", fontSize: "14px" }}>Last Name</label>
                <input 
                  type="text" 
                  value={lastName} 
                  onChange={(e) => setLastName(e.target.value)} 
                  placeholder="Enter last name" 
                  required
                  disabled={loading} 
                  style={{ width: "100%", padding: "10px", border: "1px solid #ddd", borderRadius: "4px", fontSize: "14px", boxSizing: "border-box" }} 
                />
              </div>
            </>
          )}

          <div style={{ marginBottom: "20px" }}>
            <label style={{ display: "block", marginBottom: "8px", fontWeight: "500", fontSize: "14px" }}>Username</label>
            <input 
              type="text" 
              value={username} 
              onChange={(e) => setUsername(e.target.value)} 
              placeholder="Enter username" 
              required
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
              placeholder="Enter password" 
              required
              disabled={loading} 
              style={{ width: "100%", padding: "10px", border: "1px solid #ddd", borderRadius: "4px", fontSize: "14px", boxSizing: "border-box" }} 
            />
          </div>

          <button 
            type="submit"
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
              cursor: loading ? "not-allowed" : "pointer",
              marginBottom: "16px"
            }}
          >
            {loading ? (isLogin ? "Logging in..." : "Creating account...") : (isLogin ? "Sign In" : "Create Account")}
          </button>

          <div style={{ textAlign: "center" }}>
            <button 
              type="button"
              onClick={toggleMode}
              disabled={loading}
              style={{
                background: "none",
                border: "none",
                color: "#007bff",
                cursor: loading ? "not-allowed" : "pointer",
                fontSize: "14px",
                textDecoration: "underline"
              }}
            >
              {isLogin ? "Don't have an account? Sign up" : "Already have an account? Login"}
            </button>
          </div>
        </form>

        {isLogin && (
          <div style={{ marginTop: "24px", padding: "16px", backgroundColor: "#f8f9fa", borderRadius: "4px", fontSize: "13px", color: "#666" }}>
            <p style={{ margin: "0 0 8px 0", fontWeight: "600", color: "#333" }}>Test Accounts:</p>
            <p style={{ margin: "4px 0" }}><strong>jsmith</strong> / Pass123!</p>
            <p style={{ margin: "4px 0" }}><strong>adavis</strong> / SecurePass456</p>
            <p style={{ margin: "4px 0" }}><strong>mjohnson</strong> / MyPassword789</p>
          </div>
        )}
      </div>
    </div>
  );
}