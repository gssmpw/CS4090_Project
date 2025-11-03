import urllib
from sqlalchemy import create_engine, text
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# Azure SQL connection parameters
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=cs4090.database.windows.net,1433;"
    "DATABASE=CS4090Project;"
    "UID=DevUser;"
    "PWD=CSProject4090!;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)


connection_string = f"mssql+pyodbc:///?odbc_connect={params}"
engine = create_engine(connection_string)

@app.get("/ping-db")
def ping_db():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return {"status": "connected", "result": [row[0] for row in result]}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

if __name__ == "__main__":
    # Disable reload when running directly
    uvicorn.run(app, host="127.0.0.1", port=8000)
