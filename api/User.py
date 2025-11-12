import sys
import os

# Add the parent directory to Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Union

# Import from sql folder
from sql.testSQLConnection.SQL_Functions import read_query_to_df

# Create FastAPI app for User microservice
app = FastAPI(title="User Authentication Service", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:5174"],  # Vite/React dev servers
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods including OPTIONS
    allow_headers=["*"],  # Allows all headers
)


# ============================================
# REQUEST/RESPONSE MODELS
# ============================================

class LoginRequest(BaseModel):
    username: str
    password: str


# ============================================
# AUTHENTICATION ENDPOINT
# ============================================

@app.post("/login")
async def login(request: LoginRequest) -> dict:
    """
    Authenticate a user with username and password.
    
    Returns:
        - User info dict if credentials are valid
        - 401 Unauthorized if credentials are invalid
    
    Example successful response:
    {
        "username": "jsmith",
        "Fname": "John",
        "Lname": "Smith",
        "isAdmin": false
    }
    """
    try:
        query = """
            SELECT username, Fname, Lname, isAdmin
            FROM [User]
            WHERE username = :username AND password = :password
        """
        
        df = read_query_to_df(query, {"username": request.username, "password": request.password})
        
        # If no results, credentials are invalid
        if len(df) == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        # Return user info as dictionary
        user_data = df.iloc[0].to_dict()
        return user_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during login: {str(e)}"
        )


# ============================================
# RUN THE MICROSERVICE
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)