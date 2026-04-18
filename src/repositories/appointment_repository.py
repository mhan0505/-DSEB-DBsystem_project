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
        query = """
            SELECT a.AppointmentID, a.DoctorID, a.PatientID,
                   a.AppointmentDate, a.AppointmentTime,
                   d.DoctorName, d.Specialty,
                   p.PatientName, p.PhoneNumber
            FROM Appointments a
            JOIN Doctors d ON a.DoctorID = d.DoctorID
            JOIN Patients p ON a.PatientID = p.PatientID
            ORDER BY a.AppointmentDate DESC, a.AppointmentTime
        """
        return self.db.execute_query(query)

    def get_by_id(self, appointment_id: str) -> dict:
        """
        Get appointment by ID with full details.

        TODO: SELECT with JOINs to Doctors, Departments, Patients
        """
        query = """
            SELECT a.*, d.DoctorName, d.Specialty,
                   dep.DepartmentName, p.PatientName, p.PhoneNumber
            FROM Appointments a
            JOIN Doctors d ON a.DoctorID = d.DoctorID
            JOIN Departments dep ON d.DepartmentID = dep.DepartmentID
            JOIN Patients p ON a.PatientID = p.PatientID
            WHERE a.AppointmentID = %s
        """
        results = self.db.execute_query(query, (appointment_id,))
        return results[0] if results else None

    def get_by_date(self, appointment_date) -> list:
        """
        Get appointments for a specific date.

        TODO: SELECT WHERE AppointmentDate = %s
              JOIN with Doctors and Patients for display info
        """
        query = """
            SELECT a.AppointmentID, a.AppointmentTime,
                   d.DoctorName, d.Specialty,
                   p.PatientName, p.PhoneNumber
            FROM Appointments a
            JOIN Doctors d ON a.DoctorID = d.DoctorID
            JOIN Patients p ON a.PatientID = p.PatientID
            WHERE a.AppointmentDate = %s
            ORDER BY a.AppointmentTime
        """
        return self.db.execute_query(query, (appointment_date,))

    def get_by_doctor(self, doctor_id: str) -> list:
        """
        Get all appointments for a specific doctor.

        TODO: SELECT WHERE DoctorID = %s, JOIN with Patients
        """
        query = """
            SELECT a.*, p.PatientName, p.PhoneNumber
            FROM Appointments a
            JOIN Patients p ON a.PatientID = p.PatientID
            WHERE a.DoctorID = %s
            ORDER BY a.AppointmentDate DESC, a.AppointmentTime
        """
        return self.db.execute_query(query, (doctor_id,))

    def get_by_patient(self, patient_id: str) -> list:
        """
        Get all appointments for a specific patient.

        TODO: SELECT WHERE PatientID = %s, JOIN with Doctors + Departments
        """
        query = """
            SELECT a.*, d.DoctorName, d.Specialty, dep.DepartmentName
            FROM Appointments a
            JOIN Doctors d ON a.DoctorID = d.DoctorID
            JOIN Departments dep ON d.DepartmentID = dep.DepartmentID
            WHERE a.PatientID = %s
            ORDER BY a.AppointmentDate DESC, a.AppointmentTime
        """
        return self.db.execute_query(query, (patient_id,))

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
        query = """
            SELECT COUNT(*) AS conflict_count
            FROM Appointments
            WHERE DoctorID = %s
              AND AppointmentDate = %s
              AND AppointmentTime = %s
        """
        results = self.db.execute_query(query, (doctor_id, appointment_date, appointment_time))
        return results[0]['conflict_count'] > 0

    def create(self, appointment: Appointment) -> bool:
        """
        Create a new appointment.

        TODO: INSERT INTO Appointments (AppointmentID, DoctorID, PatientID,
              AppointmentDate, AppointmentTime) VALUES (%s, %s, %s, %s, %s)
        NOTE: UNIQUE INDEX will also prevent double booking at DB level
        """
        query = """
            INSERT INTO Appointments (AppointmentID, DoctorID, PatientID, AppointmentDate, AppointmentTime)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            appointment.appointment_id, appointment.doctor_id,
            appointment.patient_id, appointment.appointment_date,
            appointment.appointment_time
        )
        affected = self.db.execute_query(query, params, fetch=False)
        return affected > 0

    def update(self, appointment: Appointment) -> bool:
        """TODO: UPDATE Appointments SET ... WHERE AppointmentID = %s"""
        query = """
            UPDATE Appointments
            SET DoctorID = %s, PatientID = %s,
                AppointmentDate = %s, AppointmentTime = %s
            WHERE AppointmentID = %s
        """
        params = (
            appointment.doctor_id, appointment.patient_id,
            appointment.appointment_date, appointment.appointment_time,
            appointment.appointment_id
        )
        affected = self.db.execute_query(query, params, fetch=False)
        return affected > 0

    def delete(self, appointment_id: str) -> bool:
        """TODO: DELETE FROM Appointments WHERE AppointmentID = %s"""
        query = "DELETE FROM Appointments WHERE AppointmentID = %s"
        affected = self.db.execute_query(query, (appointment_id,), fetch=False)
        return affected > 0

    def count(self) -> int:
        """TODO: SELECT COUNT(*)"""
        query = "SELECT COUNT(*) AS total FROM Appointments"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
