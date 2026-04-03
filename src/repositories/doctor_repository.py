"""
Doctor Repository - CRUD operations for Doctors table.
"""

from src.database_connection import DatabaseConnection
from src.models.doctor import Doctor


class DoctorRepository:
    """Data access layer for Doctor entity."""

    def __init__(self):
        self.db = DatabaseConnection()

    def get_all(self) -> list:
        """
        Get all doctors with department info.

        TODO: Write SELECT with JOIN to Departments table
        HINT: SELECT d.*, dep.DepartmentName FROM Doctors d
              JOIN Departments dep ON d.DepartmentID = dep.DepartmentID
        TODO: Return raw dict results (no conversion needed)
        """
        # TODO: Implement
        return []

    def get_by_id(self, doctor_id: str) -> Doctor:
        """
        Get doctor by ID.

        TODO: SELECT * FROM Doctors WHERE DoctorID = %s
        TODO: Return Doctor.from_dict() or None
        """
        # TODO: Implement
        return None

    def get_by_department(self, department_id: str) -> list:
        """
        Get all doctors in a department.

        TODO: SELECT WHERE DepartmentID = %s
        """
        # TODO: Implement
        return []

    def get_by_specialty(self, specialty: str) -> list:
        """
        Search doctors by specialty (partial match).

        TODO: Use LIKE with %specialty%
        """
        # TODO: Implement
        return []

    def create(self, doctor: Doctor) -> bool:
        """
        Create a new doctor.

        TODO: INSERT INTO Doctors (DoctorID, DoctorName, DepartmentID, Specialty)
        """
        # TODO: Implement
        return False

    def update(self, doctor: Doctor) -> bool:
        """
        Update an existing doctor.

        TODO: UPDATE Doctors SET ... WHERE DoctorID = %s
        """
        # TODO: Implement
        return False

    def delete(self, doctor_id: str) -> bool:
        """
        Delete a doctor by ID.

        TODO: DELETE FROM Doctors WHERE DoctorID = %s
        """
        # TODO: Implement
        return False

    def count(self) -> int:
        """Count total doctors."""
        # TODO: Implement
        return 0
