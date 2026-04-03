"""
Appointment Repository - CRUD operations for Appointments table.
⭐ Includes double booking check at database level.

This is the MOST IMPORTANT repository because it enforces
the core business rule: NO DOUBLE BOOKING.
"""

from src.database_connection import DatabaseConnection
from src.models.appointment import Appointment


class AppointmentRepository:
    """Data access layer for Appointment entity."""

    def __init__(self):
        self.db = DatabaseConnection()

    def get_all(self) -> list:
        """
        Get all appointments with doctor and patient info.

        TODO: Write SELECT with JOINs to Doctors and Patients
        HINT: SELECT a.*, d.DoctorName, d.Specialty, p.PatientName, p.PhoneNumber
              FROM Appointments a
              JOIN Doctors d ON a.DoctorID = d.DoctorID
              JOIN Patients p ON a.PatientID = p.PatientID
              ORDER BY AppointmentDate DESC, AppointmentTime
        """
        # TODO: Implement
        return []

    def get_by_id(self, appointment_id: str) -> dict:
        """
        Get appointment by ID with full details.

        TODO: SELECT with JOINs to Doctors, Departments, Patients
        """
        # TODO: Implement
        return None

    def get_by_date(self, appointment_date) -> list:
        """
        Get appointments for a specific date.

        TODO: SELECT WHERE AppointmentDate = %s
              JOIN with Doctors and Patients for display info
        """
        # TODO: Implement
        return []

    def get_by_doctor(self, doctor_id: str) -> list:
        """
        Get all appointments for a specific doctor.

        TODO: SELECT WHERE DoctorID = %s, JOIN with Patients
        """
        # TODO: Implement
        return []

    def get_by_patient(self, patient_id: str) -> list:
        """
        Get all appointments for a specific patient.

        TODO: SELECT WHERE PatientID = %s, JOIN with Doctors + Departments
        """
        # TODO: Implement
        return []

    def check_double_booking(self, doctor_id: str, appointment_date, appointment_time) -> bool:
        """
        ⭐ CRITICAL: Check if a doctor already has an appointment at the given date/time.

        Returns True if there IS a conflict (double booking detected).
        Returns False if the time slot is available.

        TODO: Write SQL to count existing appointments:
              SELECT COUNT(*) AS conflict_count FROM Appointments
              WHERE DoctorID = %s AND AppointmentDate = %s AND AppointmentTime = %s
        TODO: Return True if count > 0
        """
        # TODO: Implement - this is the most important method!
        return False

    def create(self, appointment: Appointment) -> bool:
        """
        Create a new appointment.

        TODO: INSERT INTO Appointments (AppointmentID, DoctorID, PatientID,
              AppointmentDate, AppointmentTime) VALUES (%s, %s, %s, %s, %s)
        NOTE: UNIQUE INDEX will also prevent double booking at DB level
        """
        # TODO: Implement
        return False

    def update(self, appointment: Appointment) -> bool:
        """TODO: UPDATE Appointments SET ... WHERE AppointmentID = %s"""
        # TODO: Implement
        return False

    def delete(self, appointment_id: str) -> bool:
        """TODO: DELETE FROM Appointments WHERE AppointmentID = %s"""
        # TODO: Implement
        return False

    def count(self) -> int:
        """TODO: SELECT COUNT(*)"""
        # TODO: Implement
        return 0
