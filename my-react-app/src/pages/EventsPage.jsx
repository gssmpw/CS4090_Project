import React from "react";

export default function EventsPage() {
  const events = [
    { id: 1, name: "React Workshop", date: "2025-11-15", time: "10:00 AM - 12:00 PM" },
    { id: 2, name: "AI Seminar", date: "2025-11-20", time: "2:00 PM - 4:00 PM" },
    { id: 3, name: "Hackathon", date: "2025-12-01", time: "9:00 AM - 9:00 PM" },
  ];

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        backgroundColor: "#f8f9fa",
        padding: "20px",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "500px",
          backgroundColor: "white",
          borderRadius: "8px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
          padding: "24px",
        }}
      >
        <h2 style={{ textAlign: "center", marginBottom: "24px" }}>
          Upcoming Events
        </h2>
        <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
          {events.map((event) => (
            <li
              key={event.id}
              style={{
                padding: "16px",
                borderBottom: "1px solid #e0e0e0",
                marginBottom: "8px",
              }}
            >
              <div>
                <strong style={{ fontSize: "16px" }}>{event.name}</strong>
                <br />
                <small style={{ color: "#666" }}>
                  {event.date} | {event.time}
                </small>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}