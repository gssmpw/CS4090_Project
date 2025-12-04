import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function ManageGroupsPage({ username }) {
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showEventModal, setShowEventModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showEventsListModal, setShowEventsListModal] = useState(false);
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [groupEvents, setGroupEvents] = useState([]);
  const [eventToDelete, setEventToDelete] = useState(null);
  const [eventForm, setEventForm] = useState({
    date: "",
    time: "",
    description: ""
  });
  const [eventLoading, setEventLoading] = useState(false);
  const [eventError, setEventError] = useState("");
  const [eventSuccess, setEventSuccess] = useState("");
  const [deleteLoading, setDeleteLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchAdminGroups();
  }, [username]);

  const fetchAdminGroups = async () => {
    setLoading(true);
    setError("");

    try {
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

  const fetchGroupEvents = async (groupId) => {
    try {
      const response = await fetch(`http://localhost:8002/events/group/${groupId}`);
      
      if (response.ok) {
        const data = await response.json();
        setGroupEvents(data);
      } else {
        setEventError('Failed to load events');
      }
    } catch (err) {
      console.error('Fetch events error:', err);
      setEventError('Failed to connect to server.');
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

  const handleOpenEventModal = (group, e) => {
    e.stopPropagation();
    setSelectedGroup(group);
    setShowEventModal(true);
    setEventForm({ date: "", time: "", description: "" });
    setEventError("");
    setEventSuccess("");
  };

  const handleCloseEventModal = () => {
    setShowEventModal(false);
    setSelectedGroup(null);
    setEventForm({ date: "", time: "", description: "" });
    setEventError("");
    setEventSuccess("");
  };

  const handleOpenEventsListModal = async (group, e) => {
    e.stopPropagation();
    setSelectedGroup(group);
    setShowEventsListModal(true);
    setEventError("");
    await fetchGroupEvents(group.groupID);
  };

  const handleCloseEventsListModal = () => {
    setShowEventsListModal(false);
    setSelectedGroup(null);
    setGroupEvents([]);
    setEventError("");
  };

  const handleOpenDeleteModal = (event) => {
    setEventToDelete(event);
    setShowDeleteModal(true);
  };

  const handleCloseDeleteModal = () => {
    setShowDeleteModal(false);
    setEventToDelete(null);
  };

  const handleDeleteEvent = async () => {
    setDeleteLoading(true);

    try {
      const response = await fetch(`http://localhost:8002/events/${username}/${eventToDelete.eventID}`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        // Refresh the events list
        await fetchGroupEvents(selectedGroup.groupID);
        
        // Refresh groups to update event count
        await fetchAdminGroups();
        
        handleCloseDeleteModal();
      } else {
        const errorData = await response.json();
        setEventError(errorData.detail || 'Failed to delete event');
      }
    } catch (err) {
      console.error('Delete event error:', err);
      setEventError('Failed to connect to server.');
    } finally {
      setDeleteLoading(false);
    }
  };

  const handleEventSubmit = async (e) => {
    e.preventDefault();
    setEventLoading(true);
    setEventError("");
    setEventSuccess("");

    try {
      // Combine date and time into a datetime string
      const datetime = `${eventForm.date}T${eventForm.time}:00`;
      
      const response = await fetch(`http://localhost:8002/events/group/${selectedGroup.groupID}`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          date: datetime,
          description: eventForm.description
        })
      });
      
      if (response.ok) {
        setEventSuccess('Event created successfully!');
        
        // Refresh groups to update event count
        fetchAdminGroups();
        
        // Close modal after 1.5 seconds
        setTimeout(() => {
          handleCloseEventModal();
        }, 1500);
      } else {
        const errorData = await response.json();
        setEventError(errorData.detail || 'Failed to create event');
      }
    } catch (err) {
      console.error('Create event error:', err);
      setEventError('Failed to connect to server.');
    } finally {
      setEventLoading(false);
    }
  };

  const formatDateTime = (dateString) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return dateString;
    }
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
              marginBottom: "20px",
              paddingBottom: "12px",
              borderBottom: "2px solid #e9ecef"
            }}>
              <div style={{ color: "#666", fontSize: "14px" }}>
                {groups.length} {groups.length === 1 ? 'group' : 'groups'} found
              </div>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
              {groups.map((group) => (
                <div
                  key={group.groupID}
                  style={{
                    padding: "20px",
                    border: "2px solid #e9ecef",
                    borderRadius: "8px",
                    backgroundColor: "white"
                  }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start", marginBottom: "12px" }}>
                    <div style={{ flex: 1 }}>
                      <h3 style={{ 
                        margin: "0 0 8px 0", 
                        color: "#007bff", 
                        fontSize: "18px",
                        fontWeight: "600",
                        cursor: "pointer"
                      }}
                      onClick={() => handleGroupClick(group.groupID)}
                      >
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
                  
                  <div style={{ display: "flex", gap: "8px", marginTop: "12px" }}>
                    <button
                      onClick={(e) => handleOpenEventModal(group, e)}
                      style={{
                        padding: "8px 16px",
                        backgroundColor: "#007bff",
                        color: "white",
                        border: "none",
                        borderRadius: "6px",
                        fontSize: "13px",
                        fontWeight: "600",
                        cursor: "pointer"
                      }}
                    >
                      + Add Event
                    </button>
                    <button
                      onClick={(e) => handleOpenEventsListModal(group, e)}
                      style={{
                        padding: "8px 16px",
                        backgroundColor: "#ffc107",
                        color: "white",
                        border: "none",
                        borderRadius: "6px",
                        fontSize: "13px",
                        fontWeight: "600",
                        cursor: "pointer"
                      }}
                    >
                      Manage Events
                    </button>
                    <button
                      onClick={() => handleGroupClick(group.groupID)}
                      style={{
                        padding: "8px 16px",
                        backgroundColor: "white",
                        color: "#007bff",
                        border: "2px solid #007bff",
                        borderRadius: "6px",
                        fontSize: "13px",
                        fontWeight: "600",
                        cursor: "pointer"
                      }}
                    >
                      View Details
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Event Creation Modal */}
      {showEventModal && (
        <div style={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: "rgba(0,0,0,0.5)",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          zIndex: 1000
        }}>
          <div style={{
            backgroundColor: "white",
            borderRadius: "12px",
            padding: "32px",
            maxWidth: "500px",
            width: "90%",
            maxHeight: "90vh",
            overflow: "auto"
          }}>
            <h3 style={{ margin: "0 0 8px 0", color: "#007bff", fontSize: "24px" }}>
              Create Event for {selectedGroup?.groupName}
            </h3>
            <p style={{ margin: "0 0 24px 0", color: "#666", fontSize: "14px" }}>
              Add a new event to this group
            </p>

            {eventError && (
              <div style={{ 
                padding: "12px", 
                marginBottom: "16px", 
                backgroundColor: "#f8d7da", 
                color: "#721c24", 
                borderRadius: "6px", 
                fontSize: "14px" 
              }}>
                {eventError}
              </div>
            )}

            {eventSuccess && (
              <div style={{ 
                padding: "12px", 
                marginBottom: "16px", 
                backgroundColor: "#d4edda", 
                color: "#155724", 
                borderRadius: "6px", 
                fontSize: "14px" 
              }}>
                {eventSuccess}
              </div>
            )}

            <form onSubmit={handleEventSubmit}>
              <div style={{ marginBottom: "20px" }}>
                <label style={{ 
                  display: "block", 
                  marginBottom: "8px", 
                  fontWeight: "600", 
                  fontSize: "14px",
                  color: "#333"
                }}>
                  Event Date <span style={{ color: "#dc3545" }}>*</span>
                </label>
                <input 
                  type="date" 
                  value={eventForm.date} 
                  onChange={(e) => setEventForm({...eventForm, date: e.target.value})} 
                  required
                  disabled={eventLoading} 
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

              <div style={{ marginBottom: "20px" }}>
                <label style={{ 
                  display: "block", 
                  marginBottom: "8px", 
                  fontWeight: "600", 
                  fontSize: "14px",
                  color: "#333"
                }}>
                  Event Time <span style={{ color: "#dc3545" }}>*</span>
                </label>
                <input 
                  type="time" 
                  value={eventForm.time} 
                  onChange={(e) => setEventForm({...eventForm, time: e.target.value})} 
                  required
                  disabled={eventLoading} 
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

              <div style={{ marginBottom: "24px" }}>
                <label style={{ 
                  display: "block", 
                  marginBottom: "8px", 
                  fontWeight: "600", 
                  fontSize: "14px",
                  color: "#333"
                }}>
                  Event Description <span style={{ color: "#dc3545" }}>*</span>
                </label>
                <textarea 
                  value={eventForm.description} 
                  onChange={(e) => setEventForm({...eventForm, description: e.target.value})} 
                  placeholder="Enter event description" 
                  required
                  disabled={eventLoading} 
                  rows={3}
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
              </div>

              <div style={{ display: "flex", gap: "12px" }}>
                <button 
                  type="submit"
                  disabled={eventLoading} 
                  style={{ 
                    flex: 1,
                    padding: "12px", 
                    backgroundColor: eventLoading ? "#6c757d" : "#007bff", 
                    color: "white", 
                    border: "none", 
                    borderRadius: "6px", 
                    fontSize: "16px", 
                    fontWeight: "600", 
                    cursor: eventLoading ? "not-allowed" : "pointer"
                  }}
                >
                  {eventLoading ? "Creating..." : "Create Event"}
                </button>

                <button 
                  type="button"
                  onClick={handleCloseEventModal}
                  disabled={eventLoading}
                  style={{ 
                    flex: 1,
                    padding: "12px", 
                    backgroundColor: "white",
                    color: "#6c757d", 
                    border: "2px solid #6c757d", 
                    borderRadius: "6px", 
                    fontSize: "16px", 
                    fontWeight: "600", 
                    cursor: eventLoading ? "not-allowed" : "pointer"
                  }}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Events List Modal */}
      {showEventsListModal && (
        <div style={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: "rgba(0,0,0,0.5)",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          zIndex: 1000
        }}>
          <div style={{
            backgroundColor: "white",
            borderRadius: "12px",
            padding: "32px",
            maxWidth: "600px",
            width: "90%",
            maxHeight: "90vh",
            overflow: "auto"
          }}>
            <h3 style={{ margin: "0 0 8px 0", color: "#007bff", fontSize: "24px" }}>
              Manage Events - {selectedGroup?.groupName}
            </h3>
            <p style={{ margin: "0 0 24px 0", color: "#666", fontSize: "14px" }}>
              View and delete events for this group
            </p>

            {eventError && (
              <div style={{ 
                padding: "12px", 
                marginBottom: "16px", 
                backgroundColor: "#f8d7da", 
                color: "#721c24", 
                borderRadius: "6px", 
                fontSize: "14px" 
              }}>
                {eventError}
              </div>
            )}

            {groupEvents.length === 0 ? (
              <div style={{ 
                textAlign: "center", 
                padding: "40px 20px",
                backgroundColor: "#f8f9fa",
                borderRadius: "8px"
              }}>
                <div style={{ fontSize: "48px", marginBottom: "16px" }}>📅</div>
                <p style={{ margin: 0, color: "#666", fontSize: "14px" }}>
                  No events for this group yet.
                </p>
              </div>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: "12px", marginBottom: "20px" }}>
                {groupEvents.map((event) => (
                  <div
                    key={event.eventID}
                    style={{
                      padding: "16px",
                      border: "1px solid #e9ecef",
                      borderRadius: "8px",
                      backgroundColor: "#f8f9fa",
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center"
                    }}
                  >
                    <div style={{ flex: 1 }}>
                      <div style={{ 
                        fontWeight: "600", 
                        fontSize: "16px",
                        color: "#333",
                        marginBottom: "4px"
                      }}>
                        {event.description}
                      </div>
                      <div style={{ fontSize: "14px", color: "#666" }}>
                        📅 {formatDateTime(event.date)}
                      </div>
                    </div>
                    <button
                      onClick={() => handleOpenDeleteModal(event)}
                      style={{
                        padding: "8px 16px",
                        backgroundColor: "#dc3545",
                        color: "white",
                        border: "none",
                        borderRadius: "6px",
                        fontSize: "13px",
                        fontWeight: "600",
                        cursor: "pointer"
                      }}
                    >
                      Delete
                    </button>
                  </div>
                ))}
              </div>
            )}

            <button 
              onClick={handleCloseEventsListModal}
              style={{ 
                width: "100%",
                padding: "12px", 
                backgroundColor: "#6c757d",
                color: "white", 
                border: "none", 
                borderRadius: "6px", 
                fontSize: "16px", 
                fontWeight: "600", 
                cursor: "pointer"
              }}
            >
              Close
            </button>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div style={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: "rgba(0,0,0,0.5)",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          zIndex: 1001
        }}>
          <div style={{
            backgroundColor: "white",
            borderRadius: "12px",
            padding: "32px",
            maxWidth: "400px",
            width: "90%"
          }}>
            <h3 style={{ margin: "0 0 16px 0", color: "#dc3545", fontSize: "24px" }}>
              Delete Event?
            </h3>
            <p style={{ margin: "0 0 24px 0", color: "#666", fontSize: "14px" }}>
              Are you sure you want to delete "{eventToDelete?.description}"? This action cannot be undone.
            </p>

            <div style={{ display: "flex", gap: "12px" }}>
              <button 
                onClick={handleDeleteEvent}
                disabled={deleteLoading}
                style={{ 
                  flex: 1,
                  padding: "12px", 
                  backgroundColor: deleteLoading ? "#6c757d" : "#dc3545", 
                  color: "white", 
                  border: "none", 
                  borderRadius: "6px", 
                  fontSize: "16px", 
                  fontWeight: "600", 
                  cursor: deleteLoading ? "not-allowed" : "pointer"
                }}
              >
                {deleteLoading ? "Deleting..." : "Delete"}
              </button>

              <button 
                onClick={handleCloseDeleteModal}
                disabled={deleteLoading}
                style={{ 
                  flex: 1,
                  padding: "12px", 
                  backgroundColor: "white",
                  color: "#6c757d", 
                  border: "2px solid #6c757d", 
                  borderRadius: "6px", 
                  fontSize: "16px", 
                  fontWeight: "600", 
                  cursor: deleteLoading ? "not-allowed" : "pointer"
                }}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}