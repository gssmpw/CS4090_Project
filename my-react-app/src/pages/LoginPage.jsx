import React, { useState } from "react";

export default function LoginPage({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Login attempted with:", { username, password });

    // Call the parent callback to mark the user as logged in
    onLogin();
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        backgroundColor: "#f8f9fa",
      }}
    >
      <div
        className="card shadow p-5"
        style={{
          width: "100%",
          maxWidth: "400px",
        }}
      >
        <h3 className="text-center mb-4">Login</h3>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Username</label>
            <input
              type="text"
              className="form-control"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              required
            />
          </div>

          <div className="mb-3">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-control"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
            />
          </div>

          <button type="submit" className="btn btn-primary w-100">
            Sign In
          </button>
        </form>

        {/* Optional extra links */}
        <div className="mt-3 text-center">
          <a href="#" className="text-decoration-none">
            Forgot password?
          </a>
        </div>
      </div>
    </div>
  );
}
