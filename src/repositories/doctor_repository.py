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
        query = """
            SELECT d.DoctorID, d.DoctorName, d.DepartmentID, d.Specialty,
                   dep.DepartmentName
            FROM Doctors d
            JOIN Departments dep ON d.DepartmentID = dep.DepartmentID
            ORDER BY d.DoctorID
        """
        return self.db.execute_query(query)

    def get_by_id(self, doctor_id: str) -> Doctor:
        """
        Get doctor by ID.

        TODO: SELECT * FROM Doctors WHERE DoctorID = %s
        TODO: Return Doctor.from_dict() or None
        """
        query = "SELECT * FROM Doctors WHERE DoctorID = %s"
        results = self.db.execute_query(query, (doctor_id,))
        if results:
            return Doctor.from_dict(results[0])
        return None

    def get_by_department(self, department_id: str) -> list:
        """
        Get all doctors in a department.

        TODO: SELECT WHERE DepartmentID = %s
        """
        query = "SELECT * FROM Doctors WHERE DepartmentID = %s ORDER BY DoctorName"
        results = self.db.execute_query(query, (department_id,))
        return [Doctor.from_dict(row) for row in results]

    def get_by_specialty(self, specialty: str) -> list:
        """
        Search doctors by specialty (partial match).

        TODO: Use LIKE with %specialty%
        """
        query = "SELECT * FROM Doctors WHERE Specialty LIKE %s ORDER BY DoctorName"
        results = self.db.execute_query(query, (f"%{specialty}%",))
        return [Doctor.from_dict(row) for row in results]

    def create(self, doctor: Doctor) -> bool:
        """
        Create a new doctor.

        TODO: INSERT INTO Doctors (DoctorID, DoctorName, DepartmentID, Specialty)
        """
        query = """
            INSERT INTO Doctors (DoctorID, DoctorName, DepartmentID, Specialty)
            VALUES (%s, %s, %s, %s)
        """
        params = (doctor.doctor_id, doctor.doctor_name, doctor.department_id, doctor.specialty)
        affected = self.db.execute_query(query, params, fetch=False)
        return affected > 0

    def update(self, doctor: Doctor) -> bool:
        """
        Update an existing doctor.

        TODO: UPDATE Doctors SET ... WHERE DoctorID = %s
        """
        query = """
            UPDATE Doctors
            SET DoctorName = %s, DepartmentID = %s, Specialty = %s
            WHERE DoctorID = %s
        """
        params = (doctor.doctor_name, doctor.department_id, doctor.specialty, doctor.doctor_id)
        affected = self.db.execute_query(query, params, fetch=False)
        return affected > 0

    def delete(self, doctor_id: str) -> bool:
        """
        Delete a doctor by ID.

        TODO: DELETE FROM Doctors WHERE DoctorID = %s
        """
        query = "DELETE FROM Doctors WHERE DoctorID = %s"
        affected = self.db.execute_query(query, (doctor_id,), fetch=False)
        return affected > 0

    def count(self) -> int:
        """Count total doctors."""
        query = "SELECT COUNT(*) AS total FROM Doctors"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
