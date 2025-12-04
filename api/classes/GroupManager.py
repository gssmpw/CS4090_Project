from typing import List, Dict, Any
import pandas as pd
from .SQLManager import DatabaseManager


class GroupManager:
    """
    A class for managing group-related operations in the database.
    Uses DatabaseManager for executing SQL queries and handling connections.
    """

    def __init__(self, server: str, database: str, username: str, password: str):
        """
        Initialize a GroupManager instance with an Azure SQL Database connection.
        """
        self.db = DatabaseManager(
            server=server,
            database=database,
            username=username,
            password=password
        )


    def getGroupInfoByID(self, groupIDList: List[int]) -> List[Dict[str, Any]]:
        """
        Retrieve all information for a list of group IDs.

        Args:
            groupIDList (List[int]): A list of group IDs to fetch.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries where each dictionary
                                  represents a group record.
        """
        if not groupIDList:
            return []

        placeholders = ", ".join([f":id{i}" for i in range(len(groupIDList))])
        query = f"SELECT * FROM [Group] WHERE groupID IN ({placeholders})"
        params = {f"id{i}": gid for i, gid in enumerate(groupIDList)}
        group_df: pd.DataFrame = self.db.read_query_to_df(query, params)

        return group_df.to_dict(orient="records")


    def getAllGroupIDs(self) -> List[int]:
        """
        Retrieve all group IDs from the [Group] table.

        Returns:
            List[int]: A list of all group IDs in the database.
        """
        query = "SELECT groupID FROM [Group]"
        group_df: pd.DataFrame = self.db.read_query_to_df(query)

        return group_df["groupID"].tolist() if not group_df.empty else []
