import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Import from classes folder
from classes.SQLManager import DatabaseManager

# Initialize database connection
db = DatabaseManager(
    server="cs4090.database.windows.net,1433",
    database="CS4090Project",
    username="DevUser",
    password="CSProject4090!"
)

# Create FastAPI app for Events microservice
app = FastAPI(title="Events Service", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# RESPONSE MODELS
# ============================================

class EventResponse(BaseModel):
    eventID: int
    date: str
    description: Optional[str] = None


class EventDetailResponse(BaseModel):
    eventID: int
    date: str
    description: Optional[str] = None
    groups: List[dict]  # List of groups this event belongs to


# ============================================
# EVENT ENDPOINTS
# ============================================

@app.get("/events/user/{username}")
async def get_user_events(username: str) -> List[EventResponse]:
    """
    Get all events for a specific user based on their group memberships.
    
    Returns events from all groups the user is a member of.
    """
    try:
        query = """
            SELECT DISTINCT e.eventID, e.date, CAST(e.description AS NVARCHAR(MAX)) as description
            FROM [Event] e
            JOIN GroupToEvent gte ON e.eventID = gte.eventID
            JOIN GroupMember gm ON gte.groupID = gm.groupID
            WHERE gm.username = :username
            ORDER BY e.date
        """
        
        df = db.read_query_to_df(query, {"username": username})
        
        if len(df) == 0:
            return []
        
        # Convert DataFrame to list of dictionaries
        events = df.to_dict('records')
        
        # Convert date to string format
        for event in events:
            if isinstance(event['date'], datetime):
                event['date'] = event['date'].isoformat()
        
        return events
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user events: {str(e)}"
        )


@app.get("/events/group/{group_id}")
async def get_group_events(group_id: int) -> List[EventResponse]:
    """
    Get all events for a specific group.
    
    Returns all events associated with the given group ID.
    """
    try:
        query = """
            SELECT e.eventID, e.date, CAST(e.description AS NVARCHAR(MAX)) as description
            FROM [Event] e
            JOIN GroupToEvent gte ON e.eventID = gte.eventID
            WHERE gte.groupID = :group_id
            ORDER BY e.date
        """
        
        df = db.read_query_to_df(query, {"group_id": group_id})
        
        if len(df) == 0:
            return []
        
        # Convert DataFrame to list of dictionaries
        events = df.to_dict('records')
        
        # Convert date to string format
        for event in events:
            if isinstance(event['date'], datetime):
                event['date'] = event['date'].isoformat()
        
        return events
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving group events: {str(e)}"
        )


@app.get("/events/{event_id}")
async def get_event_details(event_id: int) -> EventDetailResponse:
    """
    Get detailed information about a specific event.
    
    Includes the event details and all groups associated with it.
    """
    try:
        # Get event details
        event_query = """
            SELECT eventID, date, CAST(description AS NVARCHAR(MAX)) as description
            FROM [Event]
            WHERE eventID = :event_id
        """
        
        event_df = db.read_query_to_df(event_query, {"event_id": event_id})
        
        if len(event_df) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event with ID {event_id} not found"
            )
        
        # Get associated groups
        groups_query = """
            SELECT g.groupID, g.groupName, CAST(g.description AS NVARCHAR(MAX)) as description
            FROM [Group] g
            JOIN GroupToEvent gte ON g.groupID = gte.groupID
            WHERE gte.eventID = :event_id
        """
        
        groups_df = db.read_query_to_df(groups_query, {"event_id": event_id})
        
        # Convert event to dictionary
        event = event_df.iloc[0].to_dict()
        
        # Convert date to string format
        if isinstance(event['date'], datetime):
            event['date'] = event['date'].isoformat()
        
        # Convert groups to list of dictionaries
        groups = groups_df.to_dict('records') if len(groups_df) > 0 else []
        
        return {
            "eventID": event['eventID'],
            "date": event['date'],
            "description": event['description'],
            "groups": groups
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving event details: {str(e)}"
        )


# ============================================
# RUN THE MICROSERVICE
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)