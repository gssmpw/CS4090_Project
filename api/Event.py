import sys
import os


from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone
from classes.NotificationManager import NotificationManager

from classes.SQLManager import DatabaseManager

# Initialize NotificationManager with DB credentials
nm = NotificationManager(
    server="cs4090.database.windows.net,1433",
    database="CS4090Project",
    username="DevUser",
    password="CSProject4090!"
)


db = DatabaseManager(
    server="cs4090.database.windows.net,1433",
    database="CS4090Project",
    username="DevUser",
    password="CSProject4090!"
)

app = FastAPI(title="Events Service", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:5174", "http://127.0.0.1"],
    allow_origin_regex=r"http://localhost:\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RESPONSE MODELS

class EventResponse(BaseModel):
    eventID: int
    date: str
    description: Optional[str] = None

class EventDetailResponse(BaseModel):
    eventID: int
    date: str
    description: Optional[str] = None
    groups: List[dict]

class EventCreate(BaseModel):
    name: str
    date: str
    time: str

class EventUpdate(BaseModel):
    name: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None

class EventCreateForGroup(BaseModel):
    date: str
    description: str

class RSVPRequest(BaseModel):
    username: str

# EVENT QUERY ENDPOINTS

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
        
        event = event_df.iloc[0].to_dict()
        
        if isinstance(event['date'], datetime):
            event['date'] = event['date'].isoformat()

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

# EVENT COMMAND ENDPOINTS

@app.post("/events/{username}", status_code=status.HTTP_201_CREATED)
async def create_event(username: str, event: EventCreate):
    """
    Create a new event for a user.
    This is a temporary endpoint - will move to Groups Service.
    """
    try:
        # Verify user exists
        user_check = """
            SELECT username FROM [User] WHERE username = :username
        """
        user_df = db.read_query_to_df(user_check, {"username": username})
        
        if len(user_df) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Create event
        insert_query = """
            INSERT INTO [Event] (date, description)
            OUTPUT INSERTED.eventID
            VALUES (:date, :description)
        """
        
        # Combine date and time for description
        description = f"{event.name} at {event.time}"
        
        result_df = db.read_query_to_df(
            insert_query,
            {"date": event.date, "description": description}
        )
        
        new_event_id = result_df.iloc[0]['eventID']
        
        return {
            "id": new_event_id,
            "name": event.name,
            "date": event.date,
            "time": event.time,
            "user_id": username
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating event: {str(e)}"
        )

@app.post("/events/group/{group_id}", status_code=status.HTTP_201_CREATED)
async def create_event_for_group(group_id: int, event: EventCreateForGroup):
    """
    Create a new event for a specific group.
    """
    try:
        # Verify group exists
        group_check = """
            SELECT groupID FROM [Group] WHERE groupID = :group_id
        """
        group_df = db.read_query_to_df(group_check, {"group_id": group_id})
        
        if len(group_df) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found"
            )
        
        # Get the next available eventID
        max_id_query = "SELECT ISNULL(MAX(eventID), 0) + 1 as next_id FROM [Event]"
        max_id_df = db.read_query_to_df(max_id_query, {})
        next_event_id = int(max_id_df.iloc[0]['next_id'])
        
        # Insert new event with explicit eventID
        insert_query = """
            INSERT INTO [Event] (eventID, date, description)
            VALUES (:eventID, :date, :description)
        """
        
        db.execute_query(insert_query, {
            "eventID": next_event_id,
            "date": event.date,
            "description": event.description
        })
        
        # Link event to group in GroupToEvent table
        link_query = """
            INSERT INTO GroupToEvent (eventID, groupID)
            VALUES (:eventID, :groupID)
        """
        
        db.execute_query(link_query, {
            "eventID": next_event_id,
            "groupID": group_id
        })
        
        return {
            "eventID": next_event_id,
            "date": event.date,
            "description": event.description,
            "groupID": group_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating event: {str(e)}"
        )

@app.put("/events/{username}/{event_id}")
async def update_event(username: str, event_id: int, event: EventUpdate):
    """
    Update an existing event.
    This is a temporary endpoint - will move to Groups Service.
    """
    try:
        # Verify user exists
        user_check = """
            SELECT username FROM [User] WHERE username = :username
        """
        user_df = db.read_query_to_df(user_check, {"username": username})
        
        if len(user_df) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify event exists
        event_check = """
            SELECT eventID FROM [Event] WHERE eventID = :event_id
        """
        event_df = db.read_query_to_df(event_check, {"event_id": event_id})
        
        if len(event_df) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        
        # Build update description
        description = None
        if event.name and event.time:
            description = f"{event.name} at {event.time}"
        
        # Update event
        update_parts = []
        params = {"event_id": event_id}
        
        if event.date:
            update_parts.append("date = :date")
            params["date"] = event.date
        
        if description:
            update_parts.append("description = :description")
            params["description"] = description
        
        if not update_parts:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        update_query = f"""
            UPDATE [Event]
            SET {', '.join(update_parts)}
            WHERE eventID = :event_id
        """
        
        db.execute_query(update_query, params)
        
        return {
            "id": event_id,
            "name": event.name,
            "date": event.date,
            "time": event.time,
            "user_id": username
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating event: {str(e)}"
        )

@app.delete("/events/{username}/{event_id}")
async def delete_event(username: str, event_id: int):
    """
    Delete an event.
    This is a temporary endpoint - will move to Groups Service.
    """
    try:
        # Verify user exists
        user_check = """
            SELECT username FROM [User] WHERE username = :username
        """
        user_df = db.read_query_to_df(user_check, {"username": username})
        
        if len(user_df) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify event exists
        event_check = """
            SELECT eventID FROM [Event] WHERE eventID = :event_id
        """
        event_df = db.read_query_to_df(event_check, {"event_id": event_id})
        
        if len(event_df) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        
        # Delete from RSVP first (if exists)
        delete_rsvp = """
            DELETE FROM RSVP WHERE eventID = :event_id
        """
        db.execute_query(delete_rsvp, {"event_id": event_id})
        
        # Delete from GroupToEvent (if exists)
        delete_mapping = """
            DELETE FROM GroupToEvent WHERE eventID = :event_id
        """
        db.execute_query(delete_mapping, {"event_id": event_id})
        
        # Delete event
        delete_query = """
            DELETE FROM [Event] WHERE eventID = :event_id
        """
        db.execute_query(delete_query, {"event_id": event_id})
        
        return {
            "message": "Event deleted successfully",
            "id": event_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting event: {str(e)}"
        )

# RSVP ENDPOINTS

@app.get("/rsvp/{event_id}/{username}")
async def check_rsvp(event_id: int, username: str):
    """
    Check if a user has RSVPed to an event.
    """
    try:
        query = """
            SELECT username FROM RSVP
            WHERE eventID = :event_id AND username = :username
        """
        df = db.read_query_to_df(query, {"event_id": event_id, "username": username})
        
        return {
            "eventID": event_id,
            "username": username,
            "isRSVPed": len(df) > 0
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking RSVP: {str(e)}"
        )

@app.post("/rsvp/{event_id}", status_code=status.HTTP_201_CREATED)
async def rsvp_to_event(event_id: int, request: RSVPRequest):
    """
    RSVP to an event.
    """
    try:
        # Check if already RSVPed
        check_query = """
            SELECT username FROM RSVP
            WHERE eventID = :event_id AND username = :username
        """
        existing = db.read_query_to_df(check_query, {
            "event_id": event_id,
            "username": request.username
        })
        
        if len(existing) > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Already RSVPed to this event"
            )
        
        # Insert RSVP
        insert_query = """
            INSERT INTO RSVP (eventID, username)
            VALUES (:event_id, :username)
        """
        db.execute_query(insert_query, {
            "event_id": event_id,
            "username": request.username
        })
        
        return {
            "message": "RSVP successful",
            "eventID": event_id,
            "username": request.username
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating RSVP: {str(e)}"
        )

@app.delete("/rsvp/{event_id}/{username}")
async def un_rsvp_from_event(event_id: int, username: str):
    """
    Remove RSVP from an event.
    """
    try:
        # Check if RSVP exists
        check_query = """
            SELECT username FROM RSVP
            WHERE eventID = :event_id AND username = :username
        """
        existing = db.read_query_to_df(check_query, {
            "event_id": event_id,
            "username": username
        })
        
        if len(existing) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="RSVP not found"
            )
        
        # Delete RSVP
        delete_query = """
            DELETE FROM RSVP
            WHERE eventID = :event_id AND username = :username
        """
        db.execute_query(delete_query, {
            "event_id": event_id,
            "username": username
        })
        
        return {
            "message": "RSVP removed successfully",
            "eventID": event_id,
            "username": username
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error removing RSVP: {str(e)}"
        )

# HEALTH CHECK

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Count total events
        count_query = "SELECT COUNT(*) as total FROM [Event]"
        df = db.read_query_to_df(count_query, {})
        total_events = df.iloc[0]['total'] if len(df) > 0 else 0
        
        return {
            "status": "healthy",
            "total_events": total_events
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
    
@app.post("/events/group/{group_id}", status_code=status.HTTP_201_CREATED)
async def create_event_for_group(group_id: int, event: EventCreateForGroup):
    """
    Create a new event for a specific group.
    """
    try:
        # Verify group exists
        group_check = """
            SELECT groupID FROM [Group] WHERE groupID = :group_id
        """
        group_df = db.read_query_to_df(group_check, {"group_id": group_id})
        
        if len(group_df) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Group not found"
            )
        
        # Get the next available eventID
        max_id_query = "SELECT ISNULL(MAX(eventID), 0) + 1 as next_id FROM [Event]"
        max_id_df = db.read_query_to_df(max_id_query, {})
        next_event_id = int(max_id_df.iloc[0]['next_id'])
        
        # Insert new event with explicit eventID
        insert_query = """
            INSERT INTO [Event] (eventID, date, description)
            VALUES (:eventID, :date, :description)
        """
        
        db.execute_query(insert_query, {
            "eventID": next_event_id,
            "date": event.date,
            "description": event.description
        })
        
        # Link event to group in GroupToEvent table
        link_query = """
            INSERT INTO GroupToEvent (eventID, groupID)
            VALUES (:eventID, :groupID)
        """
        
        db.execute_query(link_query, {
            "eventID": next_event_id,
            "groupID": group_id
        })

        # Send out notifications
        try:
            nm = NotificationManager(
                server="cs4090.database.windows.net,1433",
                database="CS4090Project",
                username="DevUser",
                password="CSProject4090!"
            )

            # Fetch all group members
            members_query = "SELECT username FROM GroupMember WHERE groupID = :group_id"
            members_df = db.read_query_to_df(members_query, {"group_id": group_id})
            member_usernames = members_df["username"].tolist() if not members_df.empty else []

            # Current timestamp
            created_at = datetime.now(timezone.utc)

            # Create notifications
            nm.createNotification(
                usernames=member_usernames,
                description=event.description,
                eventID=next_event_id,
                created_at=created_at,
                eventDate=datetime.fromisoformat(event.date),
                isRead=0
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error sending notifications: {str(e)}"
            )
        
        return {
            "eventID": next_event_id,
            "date": event.date,
            "description": event.description,
            "groupID": group_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating event: {str(e)}"
        )

# RESPONSE MODEL for notifications
class NotificationResponse(BaseModel):
    notificationID: Optional[int] = None
    username: str
    description: str
    eventID: Optional[int] = None
    notificationTimestamp: datetime
    eventDate: datetime
    isRead: int

@app.get("/notifications/{username}", response_model=List[NotificationResponse])
async def get_notifications(username: str):
    """
    Get all notifications for a specific user.
    """
    try:
        notifications = nm.getNotificationsByUsername(username)
        return notifications
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving notifications: {str(e)}"
        )

def send_out_notifications(
    group_id: int,
    event_id: int,
    description: str,
    event_date: str
):
    """
    Send notifications to all group members and group admins
    when a new event is created.
    """
    try:
        # Fetch all usernames in the group
        members_query = """
            SELECT username FROM GroupMember WHERE groupID = :group_id
        """
        df = nm.db.read_query_to_df(members_query, {"group_id": group_id})
        member_usernames = df["username"].tolist() if not df.empty else []

        # Current timestamp
        created_at = datetime.utcnow()

        # Convert eventDate string to datetime if needed
        event_dt = (
            datetime.fromisoformat(event_date)
            if isinstance(event_date, str)
            else event_date
        )

        # Create notifications
        nm.createNotification(
            usernames=member_usernames,
            description=description,
            eventID=event_id,
            created_at=created_at,
            eventDate=event_dt,
            isRead=0
        )
    except Exception as e:
        raise Exception(f"Failed to send notifications: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)