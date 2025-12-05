from typing import List
import pandas as pd
from datetime import datetime, timezone
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
            query = "SELECT username FROM GroupAdmin"
            df = self.db.read_query_to_df(query)
            return df["username"].tolist() if not df.empty else []
        except Exception as e:
            raise Exception(f"Failed to fetch group admin usernames: {str(e)}")

    def createNotification(
        self,
        usernames: List[str],
        description: str,
        eventID: int,
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
                "description": description,
                "eventID": eventID,
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
        
    def getNotificationsByUsername(self, username: str):
        """
        Retrieve all notifications for a given user.

        Args:
            username (str): The username whose notifications should be fetched.

        Returns:
            List[dict]: A list of notification records, each represented as a dictionary.
        """
        try:
            query = """
                SELECT *
                FROM Notifications
                WHERE username = :username
                ORDER BY notificationTimestamp DESC
            """
            df = self.db.read_query_to_df(query, {"username": username})
            return df.to_dict("records") if not df.empty else []
        except Exception as e:
            raise Exception(f"Failed to fetch notifications for {username}: {str(e)}")

    def markNotificationAsRead(self, username: str, eventID: int) -> int:
        """
        Mark a notification as read for a specific user and event.

        Args:
            username (str): The username whose notification should be marked as read.
            eventID (int): The event ID associated with the notification.

        Returns:
            int: Number of rows updated.
        """
        try:
            query = """
                UPDATE Notifications
                SET isRead = 1
                WHERE username = :username AND eventID = :eventID
            """
            with self.db.engine.begin() as conn:
                result = conn.execute(
                    query,
                    {"username": username, "eventID": eventID}
                )
                return result.rowcount
        except Exception as e:
            raise Exception(f"Failed to mark notification as read: {str(e)}")
