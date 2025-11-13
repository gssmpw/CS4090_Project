import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function EventsPage() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [eventDetails, setEventDetails] = useState(null);
  const navigate = useNavigate();

  // Get user from sessionStorage
  const user = JSON.parse(sessionStorage.getItem('user') || '{}');
  const username = user.username;

  // Fetch user's events on component mount
  useEffect(() => {
    if (!username) {
      navigate('/');
      return;
    }
    fetchUserEvents();
  }, [username]);

  const fetchUserEvents = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch(`http://localhost:8002/events/user/${username}`);
      
      if (response.ok) {
        const data = await response.json();
        setEvents(data);
      } else {
        setError('Failed to load events');
      }
    } catch (err) {
      console.error('Error fetching events:', err);
      setError('Failed to connect to server. Make sure the backend is running on http://localhost:8002');
    } finally {
      setLoading(false);
    }
  };

  const fetchEventDetails = async (eventId) => {
    try {
      const response = await fetch(`http://localhost:8002/events/${eventId}`);
      
      if (response.ok) {
        const data = await response.json();
        setEventDetails(data);
        setSelectedEvent(eventId);
      }
    } catch (err) {
      console.error('Error fetching event details:', err);
    }
  };

  const closeModal = () => {
    setSelectedEvent(null);
    setEventDetails(null);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleLogout = () => {
    sessionStorage.removeItem('user');
    localStorage.removeItem('username');
    localStorage.removeItem('token');
    navigate('/');
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <div style={{ fontSize: '18px', color: '#666' }}>Loading events...</div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f8f9fa' }}>
      {/* Header */}
      <div style={{ 
        backgroundColor: 'white', 
        borderBottom: '1px solid #ddd', 
        padding: '16px 24px', 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center' 
      }}>
        <h1 style={{ margin: 0, fontSize: '24px' }}>My Events</h1>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <span style={{ color: '#666', fontSize: '14px' }}>
            Welcome, {user.Fname} {user.Lname}
          </span>
          <button 
            onClick={() => navigate('/dashboard')}
            style={{ 
              padding: '8px 16px', 
              backgroundColor: '#6c757d', 
              color: 'white', 
              border: 'none', 
              borderRadius: '4px', 
              cursor: 'pointer',
              fontSize: '14px'
            }}
          >
            Dashboard
          </button>
          <button 
            onClick={handleLogout}
            style={{ 
              padding: '8px 16px', 
              backgroundColor: '#dc3545', 
              color: 'white', 
              border: 'none', 
              borderRadius: '4px', 
              cursor: 'pointer',
              fontSize: '14px'
            }}
          >
            Logout
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
        {error && (
          <div style={{ 
            padding: '16px', 
            marginBottom: '24px', 
            backgroundColor: '#f8d7da', 
            color: '#721c24', 
            borderRadius: '8px', 
            border: '1px solid #f5c6cb' 
          }}>
            {error}
          </div>
        )}

        {events.length === 0 ? (
          <div style={{ 
            backgroundColor: 'white', 
            borderRadius: '8px', 
            padding: '48px', 
            textAlign: 'center',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
          }}>
            <div style={{ fontSize: '48px', marginBottom: '16px' }}>📅</div>
            <h2 style={{ marginTop: 0, marginBottom: '8px', color: '#666' }}>No Events Yet</h2>
            <p style={{ color: '#999', margin: 0 }}>You don't have any upcoming events. Join a group to see events!</p>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '20px' }}>
            {events.map((event) => (
              <div 
                key={event.eventID}
                onClick={() => fetchEventDetails(event.eventID)}
                style={{ 
                  backgroundColor: 'white', 
                  borderRadius: '8px', 
                  padding: '20px', 
                  boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                  cursor: 'pointer',
                  transition: 'transform 0.2s, box-shadow 0.2s',
                  border: '1px solid #e0e0e0'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-4px)';
                  e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', marginBottom: '12px' }}>
                  <div style={{ 
                    width: '48px', 
                    height: '48px', 
                    backgroundColor: '#007bff', 
                    borderRadius: '8px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginRight: '12px',
                    fontSize: '24px'
                  }}>
                    📅
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: '12px', color: '#666', marginBottom: '4px' }}>
                      {formatDate(event.date).split(',')[0]}
                    </div>
                    <div style={{ fontSize: '14px', fontWeight: '600', color: '#333' }}>
                      {new Date(event.date).toLocaleDateString()}
                    </div>
                  </div>
                </div>
                
                <div style={{ 
                  fontSize: '16px', 
                  fontWeight: '500', 
                  color: '#333',
                  marginBottom: '8px',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  display: '-webkit-box',
                  WebkitLineClamp: 2,
                  WebkitBoxOrient: 'vertical'
                }}>
                  {event.description || 'No description'}
                </div>
                
                <div style={{ 
                  fontSize: '13px', 
                  color: '#007bff',
                  marginTop: '12px',
                  fontWeight: '500'
                }}>
                  Click for details →
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Event Details Modal */}
      {selectedEvent && eventDetails && (
        <div 
          onClick={closeModal}
          style={{ 
            position: 'fixed', 
            top: 0, 
            left: 0, 
            right: 0, 
            bottom: 0, 
            backgroundColor: 'rgba(0,0,0,0.5)', 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center',
            zIndex: 1000
          }}
        >
          <div 
            onClick={(e) => e.stopPropagation()}
            style={{ 
              backgroundColor: 'white', 
              borderRadius: '12px', 
              padding: '32px', 
              maxWidth: '600px', 
              width: '90%',
              maxHeight: '80vh',
              overflow: 'auto',
              boxShadow: '0 8px 32px rgba(0,0,0,0.3)'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '24px' }}>
              <h2 style={{ margin: 0, fontSize: '24px', color: '#333' }}>Event Details</h2>
              <button 
                onClick={closeModal}
                style={{ 
                  background: 'none', 
                  border: 'none', 
                  fontSize: '24px', 
                  cursor: 'pointer',
                  color: '#666',
                  padding: '0',
                  width: '32px',
                  height: '32px'
                }}
              >
                ×
              </button>
            </div>

            <div style={{ marginBottom: '20px' }}>
              <div style={{ fontSize: '14px', color: '#666', marginBottom: '8px', fontWeight: '600' }}>
                DATE & TIME
              </div>
              <div style={{ fontSize: '16px', color: '#333', padding: '12px', backgroundColor: '#f8f9fa', borderRadius: '6px' }}>
                {formatDate(eventDetails.date)}
              </div>
            </div>

            <div style={{ marginBottom: '20px' }}>
              <div style={{ fontSize: '14px', color: '#666', marginBottom: '8px', fontWeight: '600' }}>
                DESCRIPTION
              </div>
              <div style={{ fontSize: '16px', color: '#333', padding: '12px', backgroundColor: '#f8f9fa', borderRadius: '6px', lineHeight: '1.6' }}>
                {eventDetails.description || 'No description available'}
              </div>
            </div>

            <div>
              <div style={{ fontSize: '14px', color: '#666', marginBottom: '8px', fontWeight: '600' }}>
                GROUPS
              </div>
              {eventDetails.groups.length > 0 ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  {eventDetails.groups.map((group) => (
                    <div 
                      key={group.groupID}
                      style={{ 
                        padding: '12px', 
                        backgroundColor: '#e7f3ff', 
                        borderRadius: '6px',
                        border: '1px solid #b8daff'
                      }}
                    >
                      <div style={{ fontSize: '16px', fontWeight: '500', color: '#004085', marginBottom: '4px' }}>
                        {group.groupName}
                      </div>
                      {group.description && (
                        <div style={{ fontSize: '14px', color: '#004085' }}>
                          {group.description}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <div style={{ padding: '12px', backgroundColor: '#f8f9fa', borderRadius: '6px', color: '#666' }}>
                  No groups associated
                </div>
              )}
            </div>

            <button 
              onClick={closeModal}
              style={{ 
                marginTop: '24px',
                width: '100%',
                padding: '12px', 
                backgroundColor: '#007bff', 
                color: 'white', 
                border: 'none', 
                borderRadius: '6px', 
                cursor: 'pointer',
                fontSize: '16px',
                fontWeight: '500'
              }}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}