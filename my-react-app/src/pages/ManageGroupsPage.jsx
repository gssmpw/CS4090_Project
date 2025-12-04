import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function ManageGroupsPage({ username }) {
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    fetchAdminGroups();
  }, [username]);

  const fetchAdminGroups = async () => {
    setLoading(true);
    setError("");

    try {
      // TODO: Replace with your actual Groups Service endpoint
      const response = await fetch(`http://localhost:8003/groups/admin/${username}`);
      
      if (response.ok) {
        const data = await response.json();
        setGroups(data);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to load groups');
      }
    } catch (err) {
      console.error('Fetch groups error:', err);
      setError('Failed to connect to server. Make sure the Groups Service is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleGroupClick = (groupId) => {
    navigate(`/group/${groupId}`);
  };

  const handleBack = () => {
    navigate('/dashboard');
  };

  const handleCreateGroup = () => {
    navigate('/create_group');
  };

  return (
    <div style={{ 
      minHeight: "100vh", 
      background: "linear-gradient(to right, #e3f2fd, #ffffff)",
      padding: "40px 20px"
    }}>
      <div style={{ 
        maxWidth: "800px", 
        margin: "0 auto",
        backgroundColor: "white", 
        borderRadius: "12px", 
        boxShadow: "0 4px 12px rgba(0,0,0,0.1)", 
        padding: "40px" 
      }}>
        <div style={{ marginBottom: "30px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <h2 style={{ margin: "0 0 8px 0", color: "#007bff", fontSize: "28px" }}>
              My Groups
            </h2>
            <p style={{ margin: 0, color: "#666", fontSize: "14px" }}>
              Groups where you are the administrator
            </p>
          </div>
          <button
            onClick={handleBack}
            style={{
              padding: "10px 20px",
              backgroundColor: "white",
              color: "#007bff",
              border: "2px solid #007bff",
              borderRadius: "6px",
              fontSize: "14px",
              fontWeight: "600",
              cursor: "pointer"
            }}
          >
            ← Back
          </button>
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

        {loading ? (
          <div style={{ textAlign: "center", padding: "40px", color: "#666" }}>
            <div style={{ fontSize: "18px" }}>Loading groups...</div>
          </div>
        ) : groups.length === 0 ? (
          <div style={{ 
            textAlign: "center", 
            padding: "60px 20px",
            backgroundColor: "#f8f9fa",
            borderRadius: "8px"
          }}>
            <div style={{ fontSize: "48px", marginBottom: "16px" }}>📁</div>
            <h3 style={{ margin: "0 0 12px 0", color: "#333" }}>
              No Groups Yet
            </h3>
            <p style={{ margin: "0 0 24px 0", color: "#666", fontSize: "14px" }}>
              You haven't created any groups yet. Create your first group to get started!
            </p>
            <button
              onClick={handleCreateGroup}
              style={{
                padding: "12px 24px",
                backgroundColor: "#28a745",
                color: "white",
                border: "none",
                borderRadius: "6px",
                fontSize: "16px",
                fontWeight: "600",
                cursor: "pointer"
              }}
            >
              Create Your First Group
            </button>
          </div>
        ) : (
          <div>
            <div style={{ 
              display: "flex", 
              justifyContent: "space-between", 
              alignItems: "center",
              marginBottom: "20px",
              paddingBottom: "12px",
              borderBottom: "2px solid #e9ecef"
            }}>
              <div style={{ color: "#666", fontSize: "14px" }}>
                {groups.length} {groups.length === 1 ? 'group' : 'groups'} found
              </div>
              <button
                onClick={handleCreateGroup}
                style={{
                  padding: "8px 16px",
                  backgroundColor: "#28a745",
                  color: "white",
                  border: "none",
                  borderRadius: "6px",
                  fontSize: "14px",
                  fontWeight: "600",
                  cursor: "pointer"
                }}
              >
                + New Group
              </button>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
              {groups.map((group) => (
                <div
                  key={group.groupID}
                  onClick={() => handleGroupClick(group.groupID)}
                  style={{
                    padding: "20px",
                    border: "2px solid #e9ecef",
                    borderRadius: "8px",
                    cursor: "pointer",
                    transition: "all 0.2s",
                    backgroundColor: "white"
                  }}
                  onMouseOver={(e) => {
                    e.currentTarget.style.borderColor = "#007bff";
                    e.currentTarget.style.backgroundColor = "#f8f9fa";
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.borderColor = "#e9ecef";
                    e.currentTarget.style.backgroundColor = "white";
                  }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start" }}>
                    <div style={{ flex: 1 }}>
                      <h3 style={{ 
                        margin: "0 0 8px 0", 
                        color: "#007bff", 
                        fontSize: "18px",
                        fontWeight: "600"
                      }}>
                        {group.groupName}
                      </h3>
                      {group.description && (
                        <p style={{ 
                          margin: "0 0 12px 0", 
                          color: "#666", 
                          fontSize: "14px",
                          lineHeight: "1.5"
                        }}>
                          {group.description}
                        </p>
                      )}
                      <div style={{ display: "flex", gap: "16px", fontSize: "13px", color: "#888" }}>
                        <span>👥 {group.memberCount || 0} members</span>
                        <span>📅 {group.eventCount || 0} events</span>
                      </div>
                    </div>
                    <div style={{
                      padding: "6px 12px",
                      backgroundColor: "#28a745",
                      color: "white",
                      borderRadius: "4px",
                      fontSize: "12px",
                      fontWeight: "600"
                    }}>
                      ADMIN
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}