import sys
import os
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException, status,Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add parent directory to path so classes can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from classes.GroupManager import GroupManager

#Group Manager class
gm = GroupManager(
    server="cs4090.database.windows.net,1433",
    database="CS4090Project",
    username="DevUser",
    password="CSProject4090!"
)

app = FastAPI(title="Group Service", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GroupResponse(BaseModel):
    groupID: int
    groupName: str
    description: str

class GroupCreate(BaseModel):
    groupName: str
    description: str
    adminUsername: str



@app.get("/groups/", response_model=List[int])
async def get_all_group_ids() -> List[int]:
    """
    Retrieve all group IDs from the database.
    """
    try:
        return gm.getAllGroupIDs()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving group IDs: {str(e)}"
        )

@app.post("/groups/by_id/", response_model=List[Dict[str, Any]])
async def get_groups_by_id(groupIDs: List[int]):
    """
    Retrieve group information for a list of group IDs.
    """
    try:
        return gm.getGroupInfoByID(groupIDs)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving group info: {str(e)}"
        )

@app.post("/groups/join/{group_id}")
async def join_group(group_id: int, username: str):
    """
    Add a user to a group.
    Example call: POST /groups/join/5?username=chase
    """
    try:
        gm.addGroupMember(username, group_id)
        return {"message": f"User {username} joined group {group_id}"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error joining group: {str(e)}"
        )


@app.post("/groups/leave/{group_id}")
async def leave_group(group_id: int, username: str):
    """
    Remove a user from a group.
    Example call: POST /groups/leave/5?username=chase
    """
    try:
        gm.removeGroupMember(username, group_id)
        return {"message": f"User {username} left group {group_id}"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error leaving group: {str(e)}"
        )
    
@app.get("/groups/user/{username}")
async def get_user_groups(username: str):
    """
    Get all groups a user is a member of.
    """
    try:
        query = """
            SELECT g.groupID, g.groupName, CAST(g.description AS NVARCHAR(MAX)) as description
            FROM [Group] g
            JOIN GroupMember gm ON g.groupID = gm.groupID
            WHERE gm.username = :username
        """
        df = gm.db.read_query_to_df(query, {"username": username})
        return df.to_dict("records")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user groups: {str(e)}"
        )

@app.get("/groups/admin/{username}")
async def get_admin_groups(username: str):
    """
    Get all groups where the user is an administrator.
    """
    try:
        query = """
            SELECT g.groupID, g.groupName, CAST(g.description AS NVARCHAR(MAX)) as description,
                   (SELECT COUNT(*) FROM GroupMember WHERE groupID = g.groupID) as memberCount,
                   (SELECT COUNT(*) FROM GroupToEvent WHERE groupID = g.groupID) as eventCount
            FROM [Group] g
            JOIN GroupAdmin ga ON g.groupID = ga.groupID
            WHERE ga.username = :username
            ORDER BY g.groupName
        """
        df = gm.db.read_query_to_df(query, {"username": username})
        return df.to_dict("records")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving admin groups: {str(e)}"
        )
    
@app.post("/groups/create", status_code=status.HTTP_201_CREATED)
async def create_group(group: GroupCreate):
    """
    Create a new group with the specified admin.
    The admin user will automatically be added as a group member and group admin.
    """
    try:
        # Check if group name already exists
        check_query = "SELECT groupID FROM [Group] WHERE groupName = :groupName"
        existing = gm.db.read_query_to_df(check_query, {"groupName": group.groupName})
        
        if len(existing) > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Group name already exists"
            )
        
        # Get the next available groupID
        max_id_query = "SELECT ISNULL(MAX(groupID), 0) + 1 as next_id FROM [Group]"
        max_id_df = gm.db.read_query_to_df(max_id_query, {})
        next_group_id = int(max_id_df.iloc[0]['next_id'])
        
        # Insert new group with explicit groupID
        insert_query = """
            INSERT INTO [Group] (groupID, groupName, description)
            VALUES (:groupID, :groupName, :description)
        """
        
        gm.db.execute_query(insert_query, {
            "groupID": next_group_id,
            "groupName": group.groupName,
            "description": group.description
        })
        
        # Add the admin to GroupMember table
        gm.addGroupMember(group.adminUsername, next_group_id)
        
        # Add the admin to GroupAdmin table
        admin_query = """
            INSERT INTO GroupAdmin (username, groupID)
            VALUES (:username, :groupID)
        """
        gm.db.execute_query(admin_query, {
            "username": group.adminUsername,
            "groupID": next_group_id
        })
        
        return {
            "groupID": next_group_id,
            "groupName": group.groupName,
            "description": group.description
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating group: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)