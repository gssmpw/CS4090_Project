from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Events API", version="1.0.0")


origins = [
    "http://localhost",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # list of origins
    allow_origin_regex=r"http://localhost:\d+",  # any port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Pydantic models
class User(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str
    token: str

class Event(BaseModel):
    id: int
    name: str
    date: str
    time: str
    user_id: str

class EventCreate(BaseModel):
    name: str
    date: str
    time: str

# In-memory users database (username: password)
users_db = {
    "john": "password123",
    "alice": "pass456",
    "bob": "test789"
}

# In-memory events database (organized by user)
events_db = {
    "john": [
        {"id": 1, "name": "React Workshop", "date": "2025-11-15", "time": "10:00 AM - 12:00 PM", "user_id": "john"},
        {"id": 2, "name": "Team Meeting", "date": "2025-11-18", "time": "3:00 PM - 4:00 PM", "user_id": "john"},
    ],
    "alice": [
        {"id": 3, "name": "AI Seminar", "date": "2025-11-20", "time": "2:00 PM - 4:00 PM", "user_id": "alice"},
        {"id": 4, "name": "Code Review", "date": "2025-11-22", "time": "10:00 AM - 11:00 AM", "user_id": "alice"},
    ],
    "bob": [
        {"id": 5, "name": "Hackathon", "date": "2025-12-01", "time": "9:00 AM - 9:00 PM", "user_id": "bob"},
    ]
}

# Counter for new event IDs
next_id = 6

# Routes
@app.get("/")
def read_root():
    return {"message": "Events API is running!", "version": "1.0.0"}

@app.post("/login", response_model=UserResponse)
def login(user: User):
    if user.username not in users_db:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    if users_db[user.username] != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Simple token (in production, use JWT)
    token = f"token_{user.username}_12345"
    
    # Create empty event list for new users
    if user.username not in events_db:
        events_db[user.username] = []
    
    return {"username": user.username, "token": token}

@app.get("/events/{username}", response_model=List[Event])
def get_user_events(username: str):
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    return events_db.get(username, [])

@app.post("/events/{username}", response_model=Event, status_code=201)
def create_event(username: str, event: EventCreate):
    global next_id
    
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Initialize user's events list if it doesn't exist
    if username not in events_db:
        events_db[username] = []
    
    new_event = {
        "id": next_id,
        "name": event.name,
        "date": event.date,
        "time": event.time,
        "user_id": username
    }
    
    events_db[username].append(new_event)
    next_id += 1
    return new_event

@app.put("/events/{username}/{event_id}", response_model=Event)
def update_event(username: str, event_id: int, event: EventCreate):
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    if username not in events_db:
        raise HTTPException(status_code=404, detail="Event not found")
    
    user_event = next((e for e in events_db[username] if e["id"] == event_id), None)
    if not user_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    user_event["name"] = event.name
    user_event["date"] = event.date
    user_event["time"] = event.time
    return user_event

@app.delete("/events/{username}/{event_id}")
def delete_event(username: str, event_id: int):
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    if username not in events_db:
        raise HTTPException(status_code=404, detail="Event not found")
    
    user_event = next((e for e in events_db[username] if e["id"] == event_id), None)
    if not user_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    events_db[username] = [e for e in events_db[username] if e["id"] != event_id]
    return {"message": "Event deleted successfully", "id": event_id}

@app.get("/health")
def health_check():
    total_events = sum(len(events) for events in events_db.values())
    return {"status": "healthy", "total_users": len(users_db), "total_events": total_events}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)