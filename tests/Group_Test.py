import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import sys
import os

# Add api folder to sys.path,  was a major issue with import issues in the original file when used in this
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "api"))

from Group import app, gm

@pytest.fixture
def client():
    return TestClient(app)


# GET /groups/
def test_get_all_group_ids_success(client):
    gm.getAllGroupIDs = MagicMock(return_value=[1, 2, 3])
    res = client.get("/groups/")
    assert res.status_code == 200
    assert res.json() == [1, 2, 3]


def test_get_all_group_ids_failure(client):
    gm.getAllGroupIDs = MagicMock(side_effect=Exception("DB error"))
    res = client.get("/groups/")
    assert res.status_code == 500
    assert "Error retrieving group IDs" in res.json()["detail"]


# POST /groups/by_id/
def test_get_groups_by_id_success(client):
    gm.getGroupInfoByID = MagicMock(return_value=[{"groupID": 1, "groupName": "Test", "description": "desc"}])
    res = client.post("/groups/by_id/", json=[1])
    assert res.status_code == 200
    assert res.json() == [{"groupID": 1, "groupName": "Test", "description": "desc"}]


def test_get_groups_by_id_failure(client):
    gm.getGroupInfoByID = MagicMock(side_effect=Exception("DB error"))
    res = client.post("/groups/by_id/", json=[1])
    assert res.status_code == 500
    assert "Error retrieving group info" in res.json()["detail"]


# POST /groups/join/{group_id}
def test_join_group_success(client):
    gm.addGroupMember = MagicMock()
    res = client.post("/groups/join/5?username=chase")
    assert res.status_code == 200
    assert res.json()["message"] == "User chase joined group 5"


def test_join_group_failure(client):
    gm.addGroupMember = MagicMock(side_effect=Exception("join error"))
    res = client.post("/groups/join/5?username=chase")
    assert res.status_code == 500
    assert "Error joining group" in res.json()["detail"]


# POST /groups/leave/{group_id}
def test_leave_group_success(client):
    gm.removeGroupMember = MagicMock()
    res = client.post("/groups/leave/5?username=chase")
    assert res.status_code == 200
    assert res.json()["message"] == "User chase left group 5"


def test_leave_group_failure(client):
    gm.removeGroupMember = MagicMock(side_effect=Exception("leave error"))
    res = client.post("/groups/leave/5?username=chase")
    assert res.status_code == 500
    assert "Error leaving group" in res.json()["detail"]


# GET /groups/user/{username}
@patch("Group.gm.db")
def test_get_user_groups_success(mock_db, client):
    mock_df = MagicMock()
    mock_df.to_dict.return_value = [{"groupID": 1, "groupName": "G", "description": "D"}]
    mock_db.read_query_to_df.return_value = mock_df

    res = client.get("/groups/user/chase")
    assert res.status_code == 200
    assert res.json() == [{"groupID": 1, "groupName": "G", "description": "D"}]


@patch("Group.gm.db")
def test_get_user_groups_failure(mock_db, client):
    mock_db.read_query_to_df.side_effect = Exception("user error")

    res = client.get("/groups/user/chase")
    assert res.status_code == 500
    assert "Error retrieving user groups" in res.json()["detail"]


# GET /groups/admin/{username}
@patch("Group.gm.db")
def test_get_admin_groups_success(mock_db, client):
    mock_df = MagicMock()
    mock_df.to_dict.return_value = [
        {"groupID": 1, "groupName": "Admins", "description": "Admin G", "memberCount": 5, "eventCount": 2}
    ]
    mock_db.read_query_to_df.return_value = mock_df

    res = client.get("/groups/admin/chase")
    assert res.status_code == 200
    assert res.json()[0]["memberCount"] == 5


@patch("Group.gm.db")
def test_get_admin_groups_failure(mock_db, client):
    mock_db.read_query_to_df.side_effect = Exception("admin error")

    res = client.get("/groups/admin/chase")
    assert res.status_code == 500
    assert "Error retrieving admin groups" in res.json()["detail"]


# POST /groups/create
@patch("Group.gm.db")
def test_create_group_success(mock_db, client):
    # group does not already exist
    mock_db.read_query_to_df.side_effect = [
        MagicMock(__len__=MagicMock(return_value=0)),  # name not used
        MagicMock(iloc=MagicMock(__getitem__=MagicMock(return_value={"next_id": 10})))  # next groupID
    ]
    mock_db.execute_query = MagicMock()
    gm.addGroupMember = MagicMock()

    payload = {"groupName": "NewGroup", "description": "Test group", "adminUsername": "chase"}
    res = client.post("/groups/create", json=payload)
    assert res.status_code == 201
    assert res.json()["groupID"] == 10
    assert res.json()["groupName"] == "NewGroup"


@patch("Group.gm.db")
def test_create_group_conflict(mock_db, client):
    mock_df = MagicMock()
    mock_df.__len__.return_value = 1
    mock_db.read_query_to_df.return_value = mock_df

    payload = {"groupName": "ExistingGroup", "description": "desc", "adminUsername": "chase"}
    res = client.post("/groups/create", json=payload)
    assert res.status_code == 409
    assert res.json()["detail"] == "Group name already exists"


@patch("Group.gm.db")
def test_create_group_failure(mock_db, client):
    mock_db.read_query_to_df.side_effect = Exception("create error")

    payload = {"groupName": "FailGroup", "description": "desc", "adminUsername": "chase"}
    res = client.post("/groups/create", json=payload)
    assert res.status_code == 500
    assert "Error creating group" in res.json()["detail"]
