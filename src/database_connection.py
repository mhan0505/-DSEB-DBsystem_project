"""
Database Connection Module - Singleton Pattern.
Manages MySQL connection lifecycle.

CONCEPTS TO LEARN:
- Singleton Pattern: Only ONE instance of this class exists
- Context Manager: Using 'with' statement for auto-cleanup
- mysql.connector: Python library to connect to MySQL
"""

import mysql.connector
from mysql.connector import Error
from src.config import DATABASE_CONFIG


class DatabaseConnection:
    """
    Database connection manager using Singleton pattern.

    Usage:
        # Method 1: Manual
        db = DatabaseConnection()
        db.connect()
        cursor = db.get_cursor()
        cursor.execute("SELECT * FROM Patients")
        db.disconnect()

        # Method 2: Context manager (recommended)
        with DatabaseConnection() as db:
            cursor = db.get_cursor()
            cursor.execute("SELECT * FROM Patients")
    """

    _instance = None

    def __new__(cls):
        """Singleton: always return the same instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def connect(self):
        """
        Establish database connection.

        TODO: Implement connection logic:
        1. Check if connection is None or not connected
        2. Use mysql.connector.connect(**DATABASE_CONFIG) to connect
        3. Print success message
        4. Handle Error exception
        HINT: self.connection = mysql.connector.connect(**DATABASE_CONFIG)
        """
        # TODO: Implement connection
        pass

    def disconnect(self):
        """
        Close database connection.

        TODO: Check if connection exists and is connected, then close it.
        HINT: if self.connection and self.connection.is_connected():
        """
        # TODO: Implement disconnection
        pass

    def get_cursor(self, dictionary=True):
        """
        Get a cursor for executing queries.

        Args:
            dictionary: If True, results come as dicts. If False, as tuples.

        TODO: If not connected, call self.connect() first.
              Then return self.connection.cursor(dictionary=dictionary)
        """
        # TODO: Ensure connection exists, then return cursor
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        return self.connection.cursor(dictionary=dictionary)

    def commit(self):
        """Commit current transaction."""
        # TODO: Call self.connection.commit()
        pass

    def rollback(self):
        """Rollback current transaction (undo changes)."""
        # TODO: Call self.connection.rollback()
        pass

    def execute_query(self, query, params=None, fetch=True):
        """
        Execute a SQL query and optionally fetch results.

        Args:
            query:  SQL string, e.g. "SELECT * FROM Patients WHERE PatientID = %s"
            params: Tuple of parameters, e.g. ('P001',)
            fetch:  If True, return results. If False, return affected row count.

        TODO: Implement:
        1. Get a cursor
        2. Execute the query with params
        3. If fetch=True: return cursor.fetchall()
        4. If fetch=False: commit and return cursor.rowcount
        5. Handle exceptions with rollback
        6. Always close cursor in finally block

        Returns:
            List of dicts (if fetch=True) or int (if fetch=False)
        """
        # TODO: Implement query execution
        if fetch:
            return []
        return 0

    def execute_procedure(self, proc_name, params=None):
        """
        Execute a stored procedure.

        Args:
            proc_name: e.g. 'sp_schedule_appointment'
            params:    Tuple of parameters

        TODO: Use cursor.callproc(proc_name, params)
              Then iterate cursor.stored_results() to get results
        """
        # TODO: Implement stored procedure execution
        return []

    def __enter__(self):
        """Context manager entry - connect to database."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - disconnect from database."""
        if exc_type:
            self.rollback()
        self.disconnect()
        DatabaseConnection._instance = None
        return False
