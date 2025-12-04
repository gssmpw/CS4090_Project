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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
