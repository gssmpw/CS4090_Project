from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from classes.SQLManager import DatabaseManager

# Create FastAPI app for User microservice
app = FastAPI(title="User Authentication Service", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = DatabaseManager(
    server="cs4090.database.windows.net,1433",
    database="CS4090Project",
    username="DevUser",
    password="CSProject4090!"
)

# ============================================
# REQUEST/RESPONSE MODELS
# ============================================

class LoginRequest(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    Fname: str  # Added - likely needed for your database
    Lname: str  # Added - likely needed for your database

class UserResponse(BaseModel):
    username: str
    Fname: str
    Lname: str
    isAdmin: bool

# ============================================
# AUTHENTICATION ENDPOINT
# ============================================

@app.post("/login")
async def login(request: LoginRequest) -> dict:
    """
    Authenticate a user with username and password.
    """
    try:
        query = """
            SELECT username, Fname, Lname, isAdmin
            FROM [User]
            WHERE username = :username AND password = :password
        """
        
        df = db.read_query_to_df(query, {"username": request.username, "password": request.password})
        
        if len(df) == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        user_data = df.iloc[0].to_dict()
        return user_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during login: {str(e)}"
        )

@app.post("/register", response_model=UserResponse, status_code=201)
async def register(user: UserCreate):
    """
    Register a new user in the database.
    """
    try:
        # Check if username already exists
        check_query = "SELECT username FROM [User] WHERE username = :username"
        existing = db.read_query_to_df(check_query, {"username": user.username})
        
        if len(existing) > 0:
            raise HTTPException(status_code=409, detail="Username already exists")
        
        # Create DataFrame with new user data
        user_df = pd.DataFrame([{
            "username": user.username,
            "password": user.password,
            "Fname": user.Fname,
            "Lname": user.Lname,
            "isAdmin": False
        }])
        
        # Insert using send_df_to_table
        db.send_df_to_table(user_df, "User", if_exists='append')
        
        return {
            "username": user.username,
            "Fname": user.Fname,
            "Lname": user.Lname,
            "isAdmin": False
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during registration: {str(e)}"
        )

# ============================================
# RUN THE MICROSERVICE
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)