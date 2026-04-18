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
        query = "SELECT * FROM Departments ORDER BY DepartmentID"
        results = self.db.execute_query(query)
        return [Department.from_dict(row) for row in results]

    def get_by_id(self, department_id: str) -> Department:
        """TODO: SELECT WHERE DepartmentID = %s"""
        query = "SELECT * FROM Departments WHERE DepartmentID = %s"
        results = self.db.execute_query(query, (department_id,))
        if results:
            return Department.from_dict(results[0])
        return None

    def create(self, department: Department) -> bool:
        """TODO: INSERT INTO Departments VALUES (%s, %s)"""
        query = "INSERT INTO Departments (DepartmentID, DepartmentName) VALUES (%s, %s)"
        affected = self.db.execute_query(query, (department.department_id, department.department_name), fetch=False)
        return affected > 0

    def update(self, department: Department) -> bool:
        """TODO: UPDATE Departments SET DepartmentName = %s WHERE DepartmentID = %s"""
        query = "UPDATE Departments SET DepartmentName = %s WHERE DepartmentID = %s"
        affected = self.db.execute_query(query, (department.department_name, department.department_id), fetch=False)
        return affected > 0

    def delete(self, department_id: str) -> bool:
        """TODO: DELETE FROM Departments WHERE DepartmentID = %s"""
        query = "DELETE FROM Departments WHERE DepartmentID = %s"
        affected = self.db.execute_query(query, (department_id,), fetch=False)
        return affected > 0

    def count(self) -> int:
        """TODO: SELECT COUNT(*)"""
        query = "SELECT COUNT(*) AS total FROM Departments"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
