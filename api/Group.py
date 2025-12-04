import sys
import os
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException, status
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
