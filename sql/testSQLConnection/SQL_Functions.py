import urllib
import pandas as pd
from sqlalchemy import create_engine, text
from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any, Optional
import uvicorn
from datetime import datetime, timedelta

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

def main_populate_database():
    """
    Populate the database with sample data:
    - 3 users (2 regular, 1 admin)
    - 3 groups
    - 3 events per group (9 total events)
    - Group memberships and admin assignments
    """
    
    print("=" * 60)
    print("POPULATING DATABASE WITH SAMPLE DATA")
    print("=" * 60)
    
    # ============================================
    # 1. CREATE USERS
    # ============================================
    print("\n1. Creating Users...")
    users_df = pd.DataFrame({
        'username': ['jsmith', 'adavis', 'mjohnson', 'bwilson', 'slee', 'kbrown'],
        'password': ['Pass123!', 'SecurePass456', 'MyPassword789', 'BookLover99', 'HikePass2025', 'TechGuru!23'],
        'Fname': ['John', 'Alice', 'Michael', 'Bob', 'Sarah', 'Kelly'],
        'Lname': ['Smith', 'Davis', 'Johnson', 'Wilson', 'Lee', 'Brown'],
        'isAdmin': [False, True, False, False, False, False]  # Alice is the system admin
    })
    
    send_df_to_table(users_df, 'User', if_exists='append')
    print(f"✓ Inserted {len(users_df)} users")
    print(users_df[['username', 'Fname', 'Lname', 'isAdmin']])
    
    # ============================================
    # 2. CREATE GROUPS
    # ============================================
    print("\n2. Creating Groups...")
    groups_df = pd.DataFrame({
        'groupID': [1, 2, 3],
        'groupName': ['Book Club', 'Hiking Adventures', 'Tech Meetup'],
        'description': [
            'Monthly book discussions and literary events',
            'Weekend hiking trips and outdoor activities',
            'Technology presentations and networking events'
        ]
    })
    
    send_df_to_table(groups_df, 'Group', if_exists='append')
    print(f"✓ Inserted {len(groups_df)} groups")
    print(groups_df[['groupID', 'groupName']])
    
    # ============================================
    # 3. CREATE EVENTS
    # ============================================
    print("\n3. Creating Events...")
    
    base_date = datetime(2025, 11, 15)
    
    events_data = []
    event_id = 1
    
    # Book Club Events (Group 1)
    events_data.extend([
        (event_id, base_date, "Discussion: '1984' by George Orwell"),
        (event_id + 1, base_date + timedelta(days=30), "Author Talk: Local Fiction Writer"),
        (event_id + 2, base_date + timedelta(days=60), "Book Swap and Coffee Social")
    ])
    event_id += 3
    
    # Hiking Adventures Events (Group 2)
    events_data.extend([
        (event_id, base_date + timedelta(days=7), "Trail Hike: Eagle Peak (5 miles)"),
        (event_id + 1, base_date + timedelta(days=21), "Waterfall Trek and Picnic"),
        (event_id + 2, base_date + timedelta(days=45), "Sunrise Hike: Mountain Vista")
    ])
    event_id += 3
    
    # Tech Meetup Events (Group 3)
    events_data.extend([
        (event_id, base_date + timedelta(days=3), "AI and Machine Learning Workshop"),
        (event_id + 1, base_date + timedelta(days=17), "Cloud Computing Panel Discussion"),
        (event_id + 2, base_date + timedelta(days=38), "Networking Night: Tech Startups")
    ])
    
    events_df = pd.DataFrame(events_data, columns=['eventID', 'date', 'description'])
    
    send_df_to_table(events_df, 'Event', if_exists='append')
    print(f"✓ Inserted {len(events_df)} events")
    print(events_df[['eventID', 'description']])
    
    # ============================================
    # 4. LINK GROUPS TO EVENTS
    # ============================================
    print("\n4. Linking Groups to Events...")
    
    group_to_event_df = pd.DataFrame({
        'eventID': [1, 2, 3, 4, 5, 6, 7, 8, 9],
        'groupID': [1, 1, 1, 2, 2, 2, 3, 3, 3]
    })
    
    send_df_to_table(group_to_event_df, 'GroupToEvent', if_exists='append')
    print(f"✓ Linked {len(group_to_event_df)} events to groups")
    
    # ============================================
    # 5. ASSIGN GROUP MEMBERS
    # ============================================
    print("\n5. Assigning Group Members...")
    
    # Book Club (Group 1): Bob (admin), Alice, John
    # Hiking Adventures (Group 2): Sarah (admin), Michael, Kelly
    # Tech Meetup (Group 3): Kelly (admin), John, Alice, Michael
    group_members_df = pd.DataFrame({
        'username': ['bwilson', 'adavis', 'jsmith', 
                     'slee', 'mjohnson', 'kbrown',
                     'kbrown', 'jsmith', 'adavis', 'mjohnson'],
        'groupID': [1, 1, 1,
                    2, 2, 2,
                    3, 3, 3, 3]
    })
    
    send_df_to_table(group_members_df, 'GroupMember', if_exists='append')
    print(f"✓ Created {len(group_members_df)} group memberships")
    
    # ============================================
    # 6. ASSIGN GROUP ADMINS
    # ============================================
    print("\n6. Assigning Group Admins...")
    
    # Bob is admin of Book Club (and is a member)
    # Sarah is admin of Hiking Adventures (and is a member)
    # Kelly is admin of Tech Meetup (and is a member)
    group_admins_df = pd.DataFrame({
        'username': ['bwilson', 'slee', 'kbrown'],
        'groupID': [1, 2, 3]
    })
    
    send_df_to_table(group_admins_df, 'GroupAdmin', if_exists='append')
    print(f"✓ Assigned {len(group_admins_df)} group admins")
    
    # ============================================
    # VERIFICATION
    # ============================================
    print("\n" + "=" * 60)
    print("DATABASE POPULATION COMPLETE!")
    print("=" * 60)
    
    print("\nSummary:")
    print(f"  • {len(users_df)} users created")
    print(f"  • {len(groups_df)} groups created")
    print(f"  • {len(events_df)} events created")
    print(f"  • {len(group_to_event_df)} group-event links")
    print(f"  • {len(group_members_df)} group memberships")
    print(f"  • {len(group_admins_df)} group admins")
    
    # Query to verify the data
    print("\n" + "=" * 60)
    print("VERIFICATION QUERIES")
    print("=" * 60)
    
    print("\nGroups with their events:")
    verification_query = """
        SELECT 
            g.groupName,
            COUNT(gte.eventID) as EventCount,
            STRING_AGG(CAST(e.eventID AS VARCHAR), ', ') as EventIDs
        FROM [Group] g
        LEFT JOIN GroupToEvent gte ON g.groupID = gte.groupID
        LEFT JOIN Event e ON gte.eventID = e.eventID
        GROUP BY g.groupName
        ORDER BY g.groupName
    """
    
    try:
        result_df = read_query_to_df(verification_query)
        print(result_df)
    except Exception as e:
        print(f"Verification query failed: {e}")
    
    print("\n✓ All data successfully populated!")

if __name__ == "__main__":
    # Uncomment the one you want to test:
    main_populate_database()