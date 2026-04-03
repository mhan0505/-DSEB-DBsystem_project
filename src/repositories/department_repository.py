"""
Department Repository - CRUD operations for Departments table.
"""

from src.database_connection import DatabaseConnection
from src.models.department import Department


class DepartmentRepository:
    """Data access layer for Department entity."""

    def __init__(self):
        self.db = DatabaseConnection()

    def get_all(self) -> list:
        """
        Get all departments.

        TODO: SELECT * FROM Departments ORDER BY DepartmentID
        TODO: Convert to list of Department objects
        """
        # TODO: Implement
        return []

    def get_by_id(self, department_id: str) -> Department:
        """TODO: SELECT WHERE DepartmentID = %s"""
        # TODO: Implement
        return None

    def create(self, department: Department) -> bool:
        """TODO: INSERT INTO Departments VALUES (%s, %s)"""
        # TODO: Implement
        return False

    def update(self, department: Department) -> bool:
        """TODO: UPDATE Departments SET DepartmentName = %s WHERE DepartmentID = %s"""
        # TODO: Implement
        return False

    def delete(self, department_id: str) -> bool:
        """TODO: DELETE FROM Departments WHERE DepartmentID = %s"""
        # TODO: Implement
        return False

    def count(self) -> int:
        """TODO: SELECT COUNT(*)"""
        # TODO: Implement
        return 0
