import sys
import os
import pandas as pd
from fastapi import FastAPI
from datetime import datetime, timedelta

# Add the path to the api/classes directory so Python can find SQLManager.py
sys.path.append(os.path.join(os.path.dirname(__file__), "api", "classes"))

####################################################################
# Pathing may be wrong, the DatabaseManager was moved into the classes folder in api
####################################################################

# Import your DatabaseManager class
from SQLManager import DatabaseManager

app = FastAPI()

# Initialize db connection
db = DatabaseManager(
    server="cs4090.database.windows.net,1433",
    database="CS4090Project",
    username="DevUser",
    password="CSProject4090!"
)

# Population functions

def main_test_read():
    print("Testing read_query_to_df()...")
    df = db.read_query_to_df("SELECT * FROM TestTable")
    print(f"Retrieved {len(df)} rows from TestTable")
    print(df.head())


def main_test_write():
    print("Testing send_df_to_table()...")
    test_df = pd.DataFrame({
        'checkValue': [True, True, False, True, False]
    })
    print("DataFrame to insert:")
    print(test_df)

    rows = db.send_df_to_table(test_df, 'TestTable', if_exists='append')
    print(f"\nInserted {rows} rows into TestTable")

    df_verify = db.read_query_to_df("SELECT * FROM TestTable")
    print(f"\nVerification - Retrieved {len(df_verify)} rows:")
    print(df_verify)


def main_populate_database():
    print("=" * 60)
    print("POPULATING DATABASE WITH SAMPLE DATA")
    print("=" * 60)

    # 1. USERS
    print("\n1. Creating Users...")
    users_df = pd.DataFrame({
        'username': ['jsmith', 'adavis', 'mjohnson', 'bwilson', 'slee', 'kbrown'],
        'password': ['Pass123!', 'SecurePass456', 'MyPassword789', 'BookLover99', 'HikePass2025', 'TechGuru!23'],
        'Fname': ['John', 'Alice', 'Michael', 'Bob', 'Sarah', 'Kelly'],
        'Lname': ['Smith', 'Davis', 'Johnson', 'Wilson', 'Lee', 'Brown'],
        'isAdmin': [False, True, False, False, False, False]
    })
    db.send_df_to_table(users_df, 'User', if_exists='append')
    print(f"✓ Inserted {len(users_df)} users")

    # 2. GROUPS
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
    db.send_df_to_table(groups_df, 'Group', if_exists='append')
    print(f"✓ Inserted {len(groups_df)} groups")

    # 3. EVENTS
    print("\n3. Creating Events...")
    base_date = datetime(2025, 11, 15)
    events_data = []
    event_id = 1

    # Book Club
    events_data.extend([
        (event_id, base_date, "Discussion: '1984' by George Orwell"),
        (event_id + 1, base_date + timedelta(days=30), "Author Talk: Local Fiction Writer"),
        (event_id + 2, base_date + timedelta(days=60), "Book Swap and Coffee Social")
    ])
    event_id += 3

    # Hiking
    events_data.extend([
        (event_id, base_date + timedelta(days=7), "Trail Hike: Eagle Peak (5 miles)"),
        (event_id + 1, base_date + timedelta(days=21), "Waterfall Trek and Picnic"),
        (event_id + 2, base_date + timedelta(days=45), "Sunrise Hike: Mountain Vista")
    ])
    event_id += 3

    # Tech Meetup
    events_data.extend([
        (event_id, base_date + timedelta(days=3), "AI and Machine Learning Workshop"),
        (event_id + 1, base_date + timedelta(days=17), "Cloud Computing Panel Discussion"),
        (event_id + 2, base_date + timedelta(days=38), "Networking Night: Tech Startups")
    ])

    events_df = pd.DataFrame(events_data, columns=['eventID', 'date', 'description'])
    db.send_df_to_table(events_df, 'Event', if_exists='append')
    print(f"✓ Inserted {len(events_df)} events")

    # 4. GROUP TO EVENT LINKS
    print("\n4. Linking Groups to Events...")
    group_to_event_df = pd.DataFrame({
        'eventID': list(range(1, 10)),
        'groupID': [1, 1, 1, 2, 2, 2, 3, 3, 3]
    })
    db.send_df_to_table(group_to_event_df, 'GroupToEvent', if_exists='append')
    print(f"✓ Linked {len(group_to_event_df)} events to groups")

    # 5. GROUP MEMBERS
    print("\n5. Assigning Group Members...")
    group_members_df = pd.DataFrame({
        'username': ['bwilson', 'adavis', 'jsmith',
                     'slee', 'mjohnson', 'kbrown',
                     'kbrown', 'jsmith', 'adavis', 'mjohnson'],
        'groupID': [1, 1, 1,
                    2, 2, 2,
                    3, 3, 3, 3]
    })
    db.send_df_to_table(group_members_df, 'GroupMember', if_exists='append')
    print(f"✓ Created {len(group_members_df)} group memberships")

    # 6. GROUP ADMINS
    print("\n6. Assigning Group Admins...")
    group_admins_df = pd.DataFrame({
        'username': ['bwilson', 'slee', 'kbrown'],
        'groupID': [1, 2, 3]
    })
    db.send_df_to_table(group_admins_df, 'GroupAdmin', if_exists='append')
    print(f"✓ Assigned {len(group_admins_df)} group admins")

    # VERIFICATION
    print("\n" + "=" * 60)
    print("DATABASE POPULATION COMPLETE!")
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
        result_df = db.read_query_to_df(verification_query)
        print(result_df)
    except Exception as e:
        print(f"Verification query failed: {e}")

    print("\n✓ All data successfully populated!")

if __name__ == "__main__":
    # Uncomment one of these:
    # main_test_read()
    # main_test_write()
    main_populate_database()
