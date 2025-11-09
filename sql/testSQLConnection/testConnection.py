import urllib
import pandas as pd
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

# Create SQLAlchemy engine
connection_string = f"mssql+pyodbc:///?odbc_connect={params}"
engine = create_engine(connection_string)

# Universal query runner
def run_query(sql: str):
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        return result.mappings().all()  # clean dict output

# Optional: Convert query result to DataFrame
def query_to_dataframe(sql: str):
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        return pd.DataFrame(result.mappings().all())

# Route: Ping database
@app.get("/ping_db")
def ping_db():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return {"status": "connected", "result": [row[0] for row in result]}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

# Route: Run test query
@app.get("/test_query")
def get_test_table():
    try:
        df = query_to_dataframe("SELECT * FROM TestTable")
        print(df.head())
        return {
            "status": "success",
            "columns": df.columns.tolist(),
            "data": df.to_dict(orient="records")
        }
    except Exception as e:
        return {"status": "failed", "error": str(e)}


# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
