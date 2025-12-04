from typing import List
import pandas as pd
from datetime import datetime
from .SQLManager import DatabaseManager

class NotificationManager:
    def __init__(self, server: str, database: str, username: str, password: str):
        self.db = DatabaseManager(
            server=server,
            database=database,
            username=username,
            password=password
        )

    def _getAllGroupAdminUsernames(self) -> List[str]:
        try:
            query = "SELECT username FROM GroupAdmins"
            df = self.db.read_query_to_df(query)
            return df["username"].tolist() if not df.empty else []
        except Exception as e:
            raise Exception(f"Failed to fetch group admin usernames: {str(e)}")

    def createNotification(
        self,
        usernames: List[str],
        title: str,
        description: str,
        groupID: int,
        created_at: datetime,
        eventDate: datetime,
        isRead: int = 0
    ) -> int:
        """
        Create notifications for a list of usernames plus all group admins.
        """
        try:
            all_admins = self._getAllGroupAdminUsernames()
            target_users = list(set(usernames + all_admins))

            df = pd.DataFrame([{
                "username": u,
                "title": title,
                "description": description,
                "groupID": groupID,
                "notificationTimestamp": created_at,   # datetime object
                "eventDate": eventDate,    # datetime object
                "isRead": isRead
            } for u in target_users])

            rows_inserted = self.db.send_df_to_table(
                df, table_name="Notifications", if_exists="append"
            )
            return rows_inserted
        except Exception as e:
            raise Exception(f"Failed to create notifications: {str(e)}")
