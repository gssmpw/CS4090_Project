import urllib
import pandas as pd
from sqlalchemy import create_engine, text
from typing import Dict, Any, Optional
import pandas as pd


class DatabaseManager:
    """
    A helper class for connecting to an Azure SQL database and performing
    read/write operations using SQLAlchemy and pandas.
    """

    def __init__(self, server: str, database: str, username: str, password: str):
        """
        Initialize the database connection.

        Args:
            server (str): SQL Server hostname (e.g., 'cs4090.database.windows.net,1433')
            database (str): Database name
            username (str): SQL login username
            password (str): SQL login password
        """
        params = urllib.parse.quote_plus(
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
            f"Connection Timeout=30;"
        )
        connection_string = f"mssql+pyodbc:///?odbc_connect={params}"
        self.engine = create_engine(connection_string)

    # QUERY FUNCTIONS
    def read_query_to_df(self, sql: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Execute a SQL query and return results as a pandas DataFrame.
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sql), params or {})
                return pd.DataFrame([dict(row) for row in result.mappings()])
        except Exception as e:
            raise Exception(f"Query to DataFrame failed: {str(e)}")

    def execute_query(self, sql: str, params: Optional[Dict[str, Any]] = None) -> None:
        """
        Execute a SQL command (INSERT, UPDATE, DELETE) without returning results.
        
        Args:
            sql (str): SQL command to execute
            params (dict): Parameters for the SQL command
        """
        try:
            with self.engine.begin() as conn:
                conn.execute(text(sql), params or {})
        except Exception as e:
            raise Exception(f"Query execution failed: {str(e)}")

    def send_df_to_table(self, df: pd.DataFrame, table_name: str, if_exists: str = 'append') -> int:
        """
        Send a pandas DataFrame to a database table.
        """
        try:
            with self.engine.begin() as conn:
                rows_inserted = df.to_sql(table_name, conn, if_exists=if_exists, index=False)
                return rows_inserted if rows_inserted else len(df)
        except Exception as e:
            raise Exception(f"DataFrame insertion failed: {str(e)}")