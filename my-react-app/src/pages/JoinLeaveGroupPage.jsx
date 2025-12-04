import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

// Separate component for each group card
function GroupTile({ group, onJoinLeave }) {
  return (
    <div
      style={{
        backgroundColor: "#f1f3f5",
        borderRadius: "8px",
        padding: "20px",
        boxShadow: "0 2px 12px rgba(0,0,0,0.2)",
        transition: "transform 0.2s, box-shadow 0.2s",
        cursor: "default",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = "translateY(-4px)";
        e.currentTarget.style.boxShadow = "0 6px 16px rgba(0,0,0,0.25)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = "translateY(0)";
        e.currentTarget.style.boxShadow = "0 2px 12px rgba(0,0,0,0.2)";
      }}
    >
      <div>
        <h3 style={{ marginTop: 0, marginBottom: "8px", color: "#212529" }}>
          {group.groupName}
        </h3>
        <p style={{ color: "#343a40", marginBottom: "12px" }}>
          {group.description || "No description"}
        </p>
      </div>

      <button
        onClick={() => onJoinLeave(group.groupID, group.joined)}
        style={{
          padding: "10px",
          backgroundColor: group.joined ? "#c82333" : "#0056b3",
          color: "white",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer",
          fontWeight: "500",
          fontSize: "14px",
          transition: "background-color 0.2s",
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.backgroundColor = group.joined
            ? "#a71d2a"
            : "#004080";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.backgroundColor = group.joined
            ? "#c82333"
            : "#0056b3";
        }}
      >
        {group.joined ? "Leave Group" : "Join Group"}
      </button>
    </div>
  );
}

export default function JoinLeaveGroupPage() {
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Get user from sessionStorage
  const user = JSON.parse(sessionStorage.getItem("user") || "{}");
  const username = user.username;

  // Fetch all groups on mount
  useEffect(() => {
    if (!username) {
      navigate("/");
      return;
    }
    fetchGroups();
  }, [username]);

  const fetchGroups = async () => {
    setLoading(true);
    setError("");
    try {
      const idsRes = await fetch("http://localhost:8003/groups/");
      if (!idsRes.ok) throw new Error("Failed to fetch group IDs");
      const groupIDs = await idsRes.json();

      if (groupIDs.length === 0) {
        setGroups([]);
        setLoading(false);
        return;
      }

      const infoRes = await fetch("http://localhost:8003/groups/by_id/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(groupIDs),
      });
      if (!infoRes.ok) throw new Error("Failed to fetch group info");
      const groupInfo = await infoRes.json();

      const updatedGroups = groupInfo.map((group) => ({
        ...group,
        joined: group.members?.includes(username) || false,
      }));

      setGroups(updatedGroups);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleJoinLeave = async (groupID, joined) => {
    try {
      const endpoint = joined
        ? `http://localhost:8003/groups/leave/${groupID}`
        : `http://localhost:8003/groups/join/${groupID}`;

      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username }),
      });

      if (!res.ok)
        throw new Error(joined ? "Failed to leave group" : "Failed to join group");

      setGroups((prev) =>
        prev.map((g) => (g.groupID === groupID ? { ...g, joined: !joined } : g))
      );
    } catch (err) {
      console.error(err);
      alert(err.message);
    }
  };

  if (loading)
    return <p style={{ textAlign: "center", marginTop: "100px" }}>Loading groups...</p>;

  if (error)
    return (
      <p style={{ textAlign: "center", marginTop: "100px", color: "red" }}>{error}</p>
    );

  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#e9ecef", padding: "24px" }}>
      <h2 style={{ textAlign: "center", color: "#212529" }}>Join or Leave Groups</h2>
      <p style={{ textAlign: "center", color: "#495057" }}>
        Manage your group memberships below
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
          gap: "20px",
          marginTop: "30px",
        }}
      >
        {groups.map((group) => (
          <GroupTile
            key={group.groupID}
            group={group}
            onJoinLeave={handleJoinLeave}
          />
        ))}
      </div>
    </div>
  );
}
