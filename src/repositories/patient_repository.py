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
        query = "SELECT * FROM Patients ORDER BY PatientID"
        results = self.db.execute_query(query)
        return [Patient.from_dict(row) for row in results]

    def get_by_id(self, patient_id: str) -> Patient:
        """
        Get a single patient by their ID.

        TODO: Write SQL "SELECT * FROM Patients WHERE PatientID = %s"
        TODO: Execute with params: (patient_id,)
        TODO: If results exist, return Patient.from_dict(results[0])
        TODO: If no results, return None
        """
        query = "SELECT * FROM Patients WHERE PatientID = %s"
        results = self.db.execute_query(query, (patient_id,))
        if results:
            return Patient.from_dict(results[0])
        return None

    def search_by_name(self, name: str) -> list:
        """
        Search patients by name (partial match).

        TODO: Use SQL LIKE: "SELECT * FROM Patients WHERE PatientName LIKE %s"
        TODO: Pass param as f"%{name}%" for partial matching
        """
        query = "SELECT * FROM Patients WHERE PatientName LIKE %s ORDER BY PatientName"
        results = self.db.execute_query(query, (f"%{name}%",))
        return [Patient.from_dict(row) for row in results]

    def create(self, patient: Patient) -> bool:
        """
        Insert a new patient into database.

        TODO: Write INSERT INTO Patients (...) VALUES (%s, %s, %s, %s, %s, %s)
        TODO: Pass patient attributes as params tuple
        TODO: Execute with fetch=False (we don't need results for INSERT)
        TODO: Return True if affected rows > 0
        """
        query = """
            INSERT INTO Patients (PatientID, PatientName, DateOfBirth, Gender, Address, PhoneNumber)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            patient.patient_id, patient.patient_name,
            patient.date_of_birth, patient.gender,
            patient.address, patient.phone_number
        )
        affected = self.db.execute_query(query, params, fetch=False)
        return affected > 0

    def update(self, patient: Patient) -> bool:
        """
        Update an existing patient.

        TODO: Write UPDATE Patients SET ... WHERE PatientID = %s
        TODO: Return True if affected rows > 0
        """
        query = """
            UPDATE Patients
            SET PatientName = %s, DateOfBirth = %s, Gender = %s,
                Address = %s, PhoneNumber = %s
            WHERE PatientID = %s
        """
        params = (
            patient.patient_name, patient.date_of_birth,
            patient.gender, patient.address,
            patient.phone_number, patient.patient_id
        )
        affected = self.db.execute_query(query, params, fetch=False)
        return affected > 0

    def delete(self, patient_id: str) -> bool:
        """
        Delete a patient by ID.

        TODO: Write DELETE FROM Patients WHERE PatientID = %s
        TODO: Return True if affected rows > 0
        NOTE: May fail if patient has appointments/invoices (FK constraint)
        """
        query = "DELETE FROM Patients WHERE PatientID = %s"
        affected = self.db.execute_query(query, (patient_id,), fetch=False)
        return affected > 0

    def count(self) -> int:
        """
        Count total patients.

        TODO: SELECT COUNT(*) AS total FROM Patients
        """
        query = "SELECT COUNT(*) AS total FROM Patients"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
