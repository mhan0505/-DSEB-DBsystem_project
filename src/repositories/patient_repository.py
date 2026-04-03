"""
Patient Repository - CRUD operations for Patients table.

CONCEPT: Repository Pattern
- This class handles ALL database operations for Patients
- Other code should NEVER write SQL for Patients directly
- Always use this repository instead
"""

from src.database_connection import DatabaseConnection
from src.models.patient import Patient


class PatientRepository:
    """Data access layer for Patient entity."""

    def __init__(self):
        self.db = DatabaseConnection()

    def get_all(self) -> list:
        """
        Get all patients from database.

        TODO: Write SQL query "SELECT * FROM Patients ORDER BY PatientID"
        TODO: Execute query using self.db.execute_query(query)
        TODO: Convert each result row to Patient using Patient.from_dict()
        TODO: Return list of Patient objects
        """
        # TODO: Implement
        return []

    def get_by_id(self, patient_id: str) -> Patient:
        """
        Get a single patient by their ID.

        TODO: Write SQL "SELECT * FROM Patients WHERE PatientID = %s"
        TODO: Execute with params: (patient_id,)
        TODO: If results exist, return Patient.from_dict(results[0])
        TODO: If no results, return None
        """
        # TODO: Implement
        return None

    def search_by_name(self, name: str) -> list:
        """
        Search patients by name (partial match).

        TODO: Use SQL LIKE: "SELECT * FROM Patients WHERE PatientName LIKE %s"
        TODO: Pass param as f"%{name}%" for partial matching
        """
        # TODO: Implement
        return []

    def create(self, patient: Patient) -> bool:
        """
        Insert a new patient into database.

        TODO: Write INSERT INTO Patients (...) VALUES (%s, %s, %s, %s, %s, %s)
        TODO: Pass patient attributes as params tuple
        TODO: Execute with fetch=False (we don't need results for INSERT)
        TODO: Return True if affected rows > 0
        """
        # TODO: Implement
        return False

    def update(self, patient: Patient) -> bool:
        """
        Update an existing patient.

        TODO: Write UPDATE Patients SET ... WHERE PatientID = %s
        TODO: Return True if affected rows > 0
        """
        # TODO: Implement
        return False

    def delete(self, patient_id: str) -> bool:
        """
        Delete a patient by ID.

        TODO: Write DELETE FROM Patients WHERE PatientID = %s
        TODO: Return True if affected rows > 0
        NOTE: May fail if patient has appointments/invoices (FK constraint)
        """
        # TODO: Implement
        return False

    def count(self) -> int:
        """
        Count total patients.

        TODO: SELECT COUNT(*) AS total FROM Patients
        """
        # TODO: Implement
        return 0
