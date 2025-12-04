import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function CreateGroupPage({ username }) {
  const [groupName, setGroupName] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const response = await fetch(`http://localhost:8003/groups/create`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          groupName,
          description,
          adminUsername: username
        })
      });
      
      if (response.ok) {
        const groupData = await response.json();
        setSuccess(`Group "${groupName}" created successfully!`);
        
        // Reset form
        setGroupName("");
        setDescription("");
        
        // Navigate to manage groups after 2 seconds
        setTimeout(() => {
          navigate('/manage_groups');
        }, 2000);
      } else {
        const errorData = await response.json();
        if (response.status === 409) {
          setError('Group name already exists. Please choose a different name.');
        } else {
          setError(errorData.detail || 'Failed to create group. Please try again.');
        }
      }
    } catch (err) {
      console.error('Create group error:', err);
      setError('Failed to connect to server. Make sure the Groups Service is running on http://localhost:8003');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    navigate('/dashboard');
  };

  return (
    <div style={{ 
      display: "flex", 
      justifyContent: "center", 
      alignItems: "center", 
      minHeight: "100vh", 
      background: "linear-gradient(to right, #e3f2fd, #ffffff)",
      padding: "20px"
    }}>
      <div style={{ 
        width: "100%", 
        maxWidth: "500px", 
        backgroundColor: "white", 
        borderRadius: "12px", 
        boxShadow: "0 4px 12px rgba(0,0,0,0.1)", 
        padding: "40px" 
      }}>
        <div style={{ marginBottom: "30px" }}>
          <h2 style={{ margin: "0 0 8px 0", color: "#007bff", fontSize: "28px" }}>
            Create New Group
          </h2>
          <p style={{ margin: 0, color: "#666", fontSize: "14px" }}>
            Create a group and become its administrator
          </p>
        </div>
        
        {error && (
          <div style={{ 
            padding: "12px", 
            marginBottom: "20px", 
            backgroundColor: "#f8d7da", 
            color: "#721c24", 
            borderRadius: "6px", 
            border: "1px solid #f5c6cb", 
            fontSize: "14px" 
          }}>
            {error}
          </div>
        )}

        {success && (
          <div style={{ 
            padding: "12px", 
            marginBottom: "20px", 
            backgroundColor: "#d4edda", 
            color: "#155724", 
            borderRadius: "6px", 
            border: "1px solid #c3e6cb", 
            fontSize: "14px" 
          }}>
            {success}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: "20px" }}>
            <label style={{ 
              display: "block", 
              marginBottom: "8px", 
              fontWeight: "600", 
              fontSize: "14px",
              color: "#333"
            }}>
              Group Name <span style={{ color: "#dc3545" }}>*</span>
            </label>
            <input 
              type="text" 
              value={groupName} 
              onChange={(e) => setGroupName(e.target.value)} 
              placeholder="Enter group name" 
              required
              disabled={loading} 
              maxLength={100}
              style={{ 
                width: "100%", 
                padding: "12px", 
                border: "1px solid #ddd", 
                borderRadius: "6px", 
                fontSize: "14px", 
                boxSizing: "border-box"
              }} 
            />
          </div>

          <div style={{ marginBottom: "28px" }}>
            <label style={{ 
              display: "block", 
              marginBottom: "8px", 
              fontWeight: "600", 
              fontSize: "14px",
              color: "#333"
            }}>
              Description
            </label>
            <textarea 
              value={description} 
              onChange={(e) => setDescription(e.target.value)} 
              placeholder="Enter group description (optional)" 
              disabled={loading} 
              rows={4}
              maxLength={500}
              style={{ 
                width: "100%", 
                padding: "12px", 
                border: "1px solid #ddd", 
                borderRadius: "6px", 
                fontSize: "14px", 
                boxSizing: "border-box",
                resize: "vertical",
                fontFamily: "inherit"
              }} 
            />
            <div style={{ 
              marginTop: "4px", 
              fontSize: "12px", 
              color: "#666", 
              textAlign: "right" 
            }}>
              {description.length}/500 characters
            </div>
          </div>

          <div style={{ display: "flex", gap: "12px" }}>
            <button 
              type="submit"
              disabled={loading || !groupName.trim()} 
              style={{ 
                flex: 1,
                padding: "12px", 
                backgroundColor: (loading || !groupName.trim()) ? "#6c757d" : "#28a745", 
                color: "white", 
                border: "none", 
                borderRadius: "6px", 
                fontSize: "16px", 
                fontWeight: "600", 
                cursor: (loading || !groupName.trim()) ? "not-allowed" : "pointer"
              }}
            >
              {loading ? "Creating..." : "Create Group"}
            </button>

            <button 
              type="button"
              onClick={handleCancel}
              disabled={loading}
              style={{ 
                flex: 1,
                padding: "12px", 
                backgroundColor: "white",
                color: "#007bff", 
                border: "2px solid #007bff", 
                borderRadius: "6px", 
                fontSize: "16px", 
                fontWeight: "600", 
                cursor: loading ? "not-allowed" : "pointer"
              }}
            >
              Cancel
            </button>
          </div>
        </form>

        <div style={{ 
          marginTop: "24px", 
          padding: "16px", 
          backgroundColor: "#f8f9fa", 
          borderRadius: "6px", 
          fontSize: "13px", 
          color: "#666" 
        }}>
          <p style={{ margin: "0 0 8px 0", fontWeight: "600", color: "#333" }}>
            ℹ️ About Groups:
          </p>
          <p style={{ margin: "4px 0" }}>
            • You will be automatically set as the group administrator
          </p>
          <p style={{ margin: "4px 0" }}>
            • You can add members and manage the group after creation
          </p>
          <p style={{ margin: "4px 0" }}>
            • Group names must be unique
          </p>
        </div>
      </div>
    </div>
  );
}