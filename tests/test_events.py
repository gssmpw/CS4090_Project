import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import sys
import os

# Add api folder to sys.path so imports work
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "api"))

from Event import app, db, nm, EventCreate, EventUpdate, EventCreateForGroup, RSVPRequest

@pytest.fixture
def client():
    return TestClient(app)


# ------------------------------
# GET /events/user/{username}
# ------------------------------
@patch("Event.db.read_query_to_df")
def test_get_user_events_success(mock_read_query, client):
    """Test retrieving events for a valid user"""
    mock_df = MagicMock()
    
    # CORRECT: Make len(mock_df) return an actual integer
    mock_df.__len__.return_value = 1
    
    # Mock to_dict('records')
    mock_df.to_dict.return_value = [
        {"eventID": 1, "date": "2025-12-09T12:00:00", "description": "Test Event"}
    ]
    
    mock_read_query.return_value = mock_df

    res = client.get("/events/user/testuser")
    assert res.status_code == 200
    assert res.json() == [
        {"eventID": 1, "date": "2025-12-09T12:00:00", "description": "Test Event"}
    ]


@patch("Event.db.read_query_to_df")
def test_get_user_events_failure(mock_read_query, client):
    mock_read_query.side_effect = Exception("DB error")

    res = client.get("/events/user/testuser")
    assert res.status_code == 500
    assert "Error retrieving user events" in res.json()["detail"]


# ------------------------------
# POST /events/{username}
# ------------------------------
@patch("Event.db")
def test_create_event_success(mock_db, client):
    # Mock user check and next event ID
    mock_db.read_query_to_df.side_effect = [
        MagicMock(__len__=MagicMock(return_value=1)),  # user exists
        MagicMock(iloc=MagicMock(__getitem__=MagicMock(return_value={"eventID": 42})))  # next eventID
    ]
    mock_db.execute_query = MagicMock()

    payload = {"name": "Party", "date": "2025-12-20", "time": "18:00"}
    res = client.post("/events/testuser", json=payload)
    assert res.status_code == 201
    assert res.json()["id"] == 42
    assert res.json()["name"] == "Party"


@patch("Event.db.read_query_to_df")
def test_create_event_user_not_found(mock_read_query, client):
    mock_read_query.return_value = MagicMock(__len__=MagicMock(return_value=0))
    payload = {"name": "Party", "date": "2025-12-20", "time": "18:00"}
    res = client.post("/events/nonexistentuser", json=payload)
    assert res.status_code == 404
    assert res.json()["detail"] == "User not found"


# ------------------------------
# RSVP /rsvp/{event_id}
# ------------------------------
@patch("Event.db.read_query_to_df")
@patch("Event.db.execute_query")
def test_rsvp_to_event_success(mock_execute, mock_read_query, client):
    mock_read_query.return_value = MagicMock(__len__=MagicMock(return_value=0))  # not already RSVPed
    payload = {"username": "testuser"}
    res = client.post("/rsvp/1", json=payload)
    assert res.status_code == 201
    assert res.json()["message"] == "RSVP successful"


@patch("Event.db.read_query_to_df")
def test_rsvp_to_event_conflict(mock_read_query, client):
    mock_read_query.return_value = MagicMock(__len__=MagicMock(return_value=1))  # already RSVPed
    payload = {"username": "testuser"}
    res = client.post("/rsvp/1", json=payload)
    assert res.status_code == 409
    assert res.json()["detail"] == "Already RSVPed to this event"


# ------------------------------
# DELETE /events/{username}/{event_id}
# ------------------------------
@patch("Event.db.read_query_to_df")
@patch("Event.db.execute_query")
def test_delete_event_success(mock_execute, mock_read_query, client):
    mock_read_query.side_effect = [
        MagicMock(__len__=MagicMock(return_value=1)),  # user exists
        MagicMock(__len__=MagicMock(return_value=1))   # event exists
    ]
    res = client.delete("/events/testuser/1")
    assert res.status_code == 200
    assert res.json()["message"] == "Event deleted successfully"
