# FastAPI + Azure SQL Connection Test

Minimal FastAPI app to test connectivity to Azure SQL using a pre-provisioned SQL login.

## Prerequisites

- Python 3.9+
- ODBC Driver 18 for SQL Server  
  Download: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy pyodbc
```

## Dev Credentials

| Key       | Value                         |
|-----------|-------------------------------|
| Server    | cs4090.database.windows.net   |
| Database  | CS4090Project                 |
| Username  | DevUser                       |
| Password  | CSProject4090!                |


## Test the Connection

Start the server:

```bash
python testConnection.py
```

Ping the endpoint:

```bash
curl http://127.0.0.1:8000/ping-db
```

Expected output:

```json
{"status":"connected","result":[1]}
```

## Notes

- This setup assumes `DevUser` has already been created and granted access to `CS4090Project`.
- Do not use these credentials in production.
