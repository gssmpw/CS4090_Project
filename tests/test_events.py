"""
Event Service Test Suite - Streamlined Coverage

File Name: test_Event.py

This test file uses mocks to test the Event service without requiring a database connection.
All database calls are mocked to return controlled test data.

Setup Instructions:
1. Install: pip install pytest
2. Place this file in the tests/ directory
3. Run: pytest test_Event.py -v
"""

import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from datetime import datetime
import sys
import os

# Mock the database and notification modules BEFORE importing Event - big issue was here
sys.modules['classes'] = MagicMock()
sys.modules['classes.SQLManager'] = MagicMock()
sys.modules['classes.NotificationManager'] = MagicMock()

# Add api folder to sys.path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "api"))

from Event import app, EventCreate, EventUpdate, EventCreateForGroup, RSVPRequest

@pytest.fixture
def client():
    """Create test client for FastAPI app"""
    return TestClient(app)

@pytest.fixture
def mock_db():
    """Create a mock database object"""
    with patch("Event.db") as mock:
        yield mock

@pytest.fixture
def mock_nm():
    """Create a mock notification manager object"""
    with patch("Event.nm") as mock:
        yield mock


# get events username

def test_get_user_events_success(client, mock_db):
    """Test retrieving events for a valid user"""
    mock_df = MagicMock()
    mock_df.__len__.return_value = 1
    mock_df.to_dict.return_value = [
        {"eventID": 1, "date": "2025-12-09T12:00:00", "description": "Test Event"}
    ]
    mock_db.read_query_to_df.return_value = mock_df

    res = client.get("/events/user/testuser")
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_get_user_events_empty(client, mock_db):
    """Test retrieving events when user has no events"""
    mock_df = MagicMock()
    mock_df.__len__.return_value = 0
    mock_db.read_query_to_df.return_value = mock_df

    res = client.get("/events/user/testuser")
    assert res.status_code == 200
    assert res.json() == []


def test_get_user_events_failure(client, mock_db):
    """Test database error during user event retrieval"""
    mock_db.read_query_to_df.side_effect = Exception("DB error")

    res = client.get("/events/user/testuser")
    assert res.status_code == 500
    assert "Error retrieving user events" in res.json()["detail"]


# get events gorp

def test_get_group_events_success(client, mock_db):
    """Test retrieving events for a valid group"""
    mock_df = MagicMock()
    mock_df.__len__.return_value = 2
    mock_df.to_dict.return_value = [
        {"eventID": 1, "date": "2025-12-09T12:00:00", "description": "Group Event 1"},
        {"eventID": 2, "date": "2025-12-10T14:00:00", "description": "Group Event 2"}
    ]
    mock_db.read_query_to_df.return_value = mock_df

    res = client.get("/events/group/1")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_get_group_events_failure(client, mock_db):
    """Test database error during group event retrieval"""
    mock_db.read_query_to_df.side_effect = Exception("DB error")

    res = client.get("/events/group/1")
    assert res.status_code == 500
    assert "Error retrieving group events" in res.json()["detail"]


# get events

def test_get_event_details_success(client, mock_db):
    """Test retrieving details for a specific event"""
    event_df = MagicMock()
    event_df.__len__.return_value = 1
    event_df.iloc = [MagicMock(to_dict=MagicMock(return_value={
        "eventID": 1,
        "date": "2025-12-09T12:00:00",
        "description": "Test Event"
    }))]
    
    groups_df = MagicMock()
    groups_df.__len__.return_value = 1
    groups_df.to_dict.return_value = [
        {"groupID": 1, "groupName": "Test Group", "description": "Test Group Desc"}
    ]
    
    mock_db.read_query_to_df.side_effect = [event_df, groups_df]

    res = client.get("/events/1")
    assert res.status_code == 200
    assert res.json()["eventID"] == 1
    assert len(res.json()["groups"]) == 1


def test_get_event_details_not_found(client, mock_db):
    """Test retrieving details for non-existent event"""
    mock_df = MagicMock()
    mock_df.__len__.return_value = 0
    mock_db.read_query_to_df.return_value = mock_df

    res = client.get("/events/999")
    assert res.status_code == 404
    assert "not found" in res.json()["detail"]


# post

def test_create_event_success(client, mock_db):
    """Test successful event creation"""
    user_df = MagicMock()
    user_df.__len__.return_value = 1
    
    result_df = MagicMock()
    result_df.iloc = [{"eventID": 42}]
    
    mock_db.read_query_to_df.side_effect = [user_df, result_df]

    payload = {"name": "Party", "date": "2025-12-20", "time": "18:00"}
    res = client.post("/events/testuser", json=payload)
    
    assert res.status_code == 201
    assert res.json()["id"] == 42


def test_create_event_user_not_found(client, mock_db):
    """Test event creation with non-existent user"""
    mock_df = MagicMock()
    mock_df.__len__.return_value = 0
    mock_db.read_query_to_df.return_value = mock_df

    payload = {"name": "Party", "date": "2025-12-20", "time": "18:00"}
    res = client.post("/events/nonexistentuser", json=payload)
    
    assert res.status_code == 404
    assert res.json()["detail"] == "User not found"


def test_create_event_missing_fields(client, mock_db):
    """Test event creation without required fields"""
    payload = {"date": "2025-12-20"}
    res = client.post("/events/testuser", json=payload)
    assert res.status_code == 422


# post

def test_create_event_for_group_success(client, mock_db, mock_nm):
    """Test successful event creation for a group"""
    group_df = MagicMock()
    group_df.__len__.return_value = 1
    
    max_id_df = MagicMock()
    max_id_df.iloc = [{"next_id": 5}]
    
    members_df = MagicMock()
    members_df.empty = False
    members_df.__getitem__ = MagicMock(return_value=MagicMock(tolist=MagicMock(return_value=["user1", "user2"])))
    
    mock_db.read_query_to_df.side_effect = [group_df, max_id_df, members_df]
    mock_db.execute_query.return_value = None
    mock_nm.createNotification.return_value = None

    payload = {"date": "2025-12-20", "description": "Group Meeting"}
    res = client.post("/events/group/1", json=payload)
    
    assert res.status_code == 201
    assert res.json()["eventID"] == 5


def test_create_event_for_group_not_found(client, mock_db):
    """Test event creation for non-existent group"""
    mock_df = MagicMock()
    mock_df.__len__.return_value = 0
    mock_db.read_query_to_df.return_value = mock_df

    payload = {"date": "2025-12-20", "description": "Group Meeting"}
    res = client.post("/events/group/999", json=payload)
    
    assert res.status_code == 404
    assert "Group not found" in res.json()["detail"]


# # put

def test_update_event_success(client, mock_db):
    """Test successful event update"""
    user_df = MagicMock()
    user_df.__len__.return_value = 1
    
    event_df = MagicMock()
    event_df.__len__.return_value = 1
    
    mock_db.read_query_to_df.side_effect = [user_df, event_df]
    mock_db.execute_query.return_value = None

    payload = {"name": "Updated Party", "date": "2025-12-21", "time": "19:00"}
    res = client.put("/events/testuser/1", json=payload)
    
    assert res.status_code == 200
    assert res.json()["name"] == "Updated Party"


def test_update_event_not_found(client, mock_db):
    """Test event update with non-existent event"""
    user_df = MagicMock()
    user_df.__len__.return_value = 1
    
    event_df = MagicMock()
    event_df.__len__.return_value = 0
    
    mock_db.read_query_to_df.side_effect = [user_df, event_df]

    payload = {"name": "Updated Party", "date": "2025-12-21", "time": "19:00"}
    res = client.put("/events/testuser/999", json=payload)
    
    assert res.status_code == 404
    assert "Event not found" in res.json()["detail"]


def test_update_event_no_fields(client, mock_db):
    """Test event update with no fields to update"""
    user_df = MagicMock()
    user_df.__len__.return_value = 1
    
    event_df = MagicMock()
    event_df.__len__.return_value = 1
    
    mock_db.read_query_to_df.side_effect = [user_df, event_df]

    payload = {}
    res = client.put("/events/testuser/1", json=payload)
    
    assert res.status_code == 400
    assert "No fields to update" in res.json()["detail"]


# Delete

def test_delete_event_success(client, mock_db):
    """Test successful event deletion"""
    user_df = MagicMock()
    user_df.__len__.return_value = 1
    
    event_df = MagicMock()
    event_df.__len__.return_value = 1
    
    mock_db.read_query_to_df.side_effect = [user_df, event_df]
    mock_db.execute_query.return_value = None

    res = client.delete("/events/testuser/1")
    
    assert res.status_code == 200
    assert res.json()["message"] == "Event deleted successfully"


def test_delete_event_not_found(client, mock_db):
    """Test event deletion with non-existent event"""
    user_df = MagicMock()
    user_df.__len__.return_value = 1
    
    event_df = MagicMock()
    event_df.__len__.return_value = 0
    
    mock_db.read_query_to_df.side_effect = [user_df, event_df]

    res = client.delete("/events/testuser/999")
    
    assert res.status_code == 404
    assert "Event not found" in res.json()["detail"]


# RSVP endpoints

def test_check_rsvp_exists(client, mock_db):
    """Test checking RSVP that exists"""
    mock_df = MagicMock()
    mock_df.__len__.return_value = 1
    mock_db.read_query_to_df.return_value = mock_df

    res = client.get("/rsvp/1/testuser")
    
    assert res.status_code == 200
    assert res.json()["isRSVPed"] == True


def test_check_rsvp_not_exists(client, mock_db):
    """Test checking RSVP that doesn't exist"""
    mock_df = MagicMock()
    mock_df.__len__.return_value = 0
    mock_db.read_query_to_df.return_value = mock_df

    res = client.get("/rsvp/1/testuser")
    
    assert res.status_code == 200
    assert res.json()["isRSVPed"] == False


def test_rsvp_to_event_success(client, mock_db):
    """Test successful RSVP to event"""
    mock_df = MagicMock()
    mock_df.__len__.return_value = 0
    mock_db.read_query_to_df.return_value = mock_df
    mock_db.execute_query.return_value = None

    payload = {"username": "testuser"}
    res = client.post("/rsvp/1", json=payload)
    
    assert res.status_code == 201
    assert res.json()["message"] == "RSVP successful"


def test_rsvp_to_event_conflict(client, mock_db):
    """Test RSVP when already RSVPed"""
    mock_df = MagicMock()
    mock_df.__len__.return_value = 1
    mock_db.read_query_to_df.return_value = mock_df

    payload = {"username": "testuser"}
    res = client.post("/rsvp/1", json=payload)
    
    assert res.status_code == 409
    assert res.json()["detail"] == "Already RSVPed to this event"


def test_un_rsvp_success(client, mock_db):
    """Test successful RSVP removal"""
    mock_df = MagicMock()
    mock_df.__len__.return_value = 1
    mock_db.read_query_to_df.return_value = mock_df
    mock_db.execute_query.return_value = None

    res = client.delete("/rsvp/1/testuser")
    
    assert res.status_code == 200
    assert res.json()["message"] == "RSVP removed successfully"


def test_un_rsvp_not_found(client, mock_db):
    """Test RSVP removal when RSVP doesn't exist"""
    mock_df = MagicMock()
    mock_df.__len__.return_value = 0
    mock_db.read_query_to_df.return_value = mock_df

    res = client.delete("/rsvp/1/testuser")
    
    assert res.status_code == 404
    assert "RSVP not found" in res.json()["detail"]


# Health and Notis

def test_health_check_healthy(client, mock_db):
    """Test health check when database is accessible"""
    mock_df = MagicMock()
    mock_df.__len__.return_value = 1
    mock_df.iloc = [{"total": 42}]
    mock_db.read_query_to_df.return_value = mock_df

    res = client.get("/health")
    
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"


def test_get_notifications_success(client, mock_nm):
    """Test successful notification retrieval"""
    mock_notifications = [
        {
            "notificationID": 1,
            "username": "testuser",
            "description": "New event created",
            "eventID": 5,
            "notificationTimestamp": datetime(2025, 12, 9, 12, 0, 0),
            "eventDate": datetime(2025, 12, 20, 18, 0, 0),
            "isRead": 0
        }
    ]
    mock_nm.getNotificationsByUsername.return_value = mock_notifications

    res = client.get("/notifications/testuser")
    
    assert res.status_code == 200
    assert len(res.json()) == 1


# Summary
if __name__ == "__main__":
    print("\n" + "="*70)
    print("Event Service Test Suite - Streamlined")
    print("="*70)
    print("\nTest Categories:")
    print("  • GET /events/user/{username} - 3 tests")
    print("  • GET /events/group/{group_id} - 2 tests")
    print("  • GET /events/{event_id} - 2 tests")
    print("  • POST /events/{username} - 3 tests")
    print("  • POST /events/group/{group_id} - 2 tests")
    print("  • PUT /events/{username}/{event_id} - 3 tests")
    print("  • DELETE /events/{username}/{event_id} - 2 tests")
    print("  • RSVP Endpoints - 6 tests")
    print("  • Health & Notifications - 2 tests")
    print("\nTotal: 25 test cases")
    print("\n✓ All tests use mocks - NO database connection required")
    print("✓ Database and NotificationManager modules completely mocked")
    print("✓ No real data will be written to any database")
    print("\nTo run these tests:")
    print("  pytest test_Event.py -v")
    print("\nTo run with output:")
    print("  pytest test_Event.py -v -s")
    print("="*70 + "\n")