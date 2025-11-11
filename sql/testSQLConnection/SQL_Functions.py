import urllib
import pandas as pd
from sqlalchemy import create_engine, text
from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any, Optional
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


# ============================================
# GENERAL DATABASE FUNCTIONS
# ============================================

def read_query_to_df(sql: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """
    Execute a SQL query and return results as a pandas DataFrame.
    
    Args:
        sql: SQL query string (use :param_name for parameters)
        params: Dictionary of parameters to bind to the query
        
    Returns:
        pandas DataFrame with query results
        
    Examples:
        # Simple query
        df = read_query_to_df("SELECT * FROM Users")
        
        # Query with parameters
        df = read_query_to_df("SELECT * FROM Users WHERE age > :min_age", {"min_age": 18})
        
        # Complex query
        df = read_query_to_df('''
            SELECT u.name, o.order_date, o.total 
            FROM Users u 
            JOIN Orders o ON u.id = o.user_id
            WHERE o.order_date > :start_date
        ''', {"start_date": "2024-01-01"})
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql), params or {})
            return pd.DataFrame([dict(row) for row in result.mappings()])
    except Exception as e:
        raise Exception(f"Query to DataFrame failed: {str(e)}")


def send_df_to_table(df: pd.DataFrame, table_name: str, if_exists: str = 'append') -> int:
    """
    Send a pandas DataFrame to a database table.
    
    Args:
        df: pandas DataFrame to insert
        table_name: Name of the target table
        if_exists: How to behave if table exists:
            - 'append': Add data to existing table (default)
            - 'replace': Drop table and create new one
            - 'fail': Raise error if table exists
        
    Returns:
        Number of rows inserted
        
    Examples:
        # Append new rows to existing table
        df = pd.DataFrame({'name': ['John', 'Jane'], 'age': [30, 25]})
        send_df_to_table(df, 'Users')
        
        # Replace entire table
        send_df_to_table(df, 'Users', if_exists='replace')
        
        # Fail if table already exists
        send_df_to_table(df, 'NewTable', if_exists='fail')
    """
    try:
        rows_inserted = df.to_sql(table_name, engine, if_exists=if_exists, index=False)
        return rows_inserted if rows_inserted else len(df)
    except Exception as e:
        raise Exception(f"DataFrame insertion failed: {str(e)}")
    
def main_test_read():
    print("Testing read_query_to_df()...")
    
    df = read_query_to_df("SELECT * FROM TestTable")
    print(f"Retrieved {len(df)} rows from TestTable")
    print(df.head())

def main_test_write():
    print("Testing send_df_to_table()...")
    
    # Create test DataFrame with boolean values
    test_df = pd.DataFrame({
        'checkValue': [True, True, False, True, False]
    })
    
    print("DataFrame to insert:")
    print(test_df)
    
    # Send to database
    rows = send_df_to_table(test_df, 'TestTable', if_exists='append')
    print(f"\nInserted {rows} rows into TestWriteTable")
    
    # Verify
    df_verify = read_query_to_df("SELECT * FROM TestTable")
    print(f"\nVerification - Retrieved {len(df_verify)} rows:")
    print(df_verify)

if __name__ == "__main__":
    # Uncomment the one you want to test:
    
    main_test_write()