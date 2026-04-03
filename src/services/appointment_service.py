"""
Appointment Service - Business Logic Layer.
⭐ CORE: Double booking prevention + appointment scheduling.

CONCEPT: Service Layer Pattern
- Repository handles database queries
- Service handles BUSINESS RULES (validation, logic)
- CLI/UI calls Service, Service calls Repository
"""

from datetime import date, time
from src.database_connection import DatabaseConnection
from src.repositories.appointment_repository import AppointmentRepository
from src.repositories.doctor_repository import DoctorRepository
from src.repositories.patient_repository import PatientRepository
from src.models.appointment import Appointment


class AppointmentService:
    """
    Business logic for appointment management.

    Key Rules:
    1. ⭐ A doctor CANNOT have 2 appointments at the same date/time
    2. Both doctor and patient must exist
    """

    def __init__(self):
        self.appt_repo = AppointmentRepository()
        self.doctor_repo = DoctorRepository()
        self.patient_repo = PatientRepository()
        self.db = DatabaseConnection()

    def schedule_appointment(
        self,
        appointment_id: str,
        doctor_id: str,
        patient_id: str,
        appointment_date: date,
        appointment_time: time
    ) -> dict:
        """
        ⭐ Schedule a new appointment with full business validation.

        TODO: Implement the following steps:

        Step 1: Validate doctor exists
            doctor = self.doctor_repo.get_by_id(doctor_id)
            If None → return {'status': 'ERROR', 'message': 'Doctor not found'}

        Step 2: Validate patient exists
            patient = self.patient_repo.get_by_id(patient_id)
            If None → return {'status': 'ERROR', 'message': 'Patient not found'}

        Step 3: ⭐ CHECK DOUBLE BOOKING
            is_conflict = self.appt_repo.check_double_booking(
                doctor_id, appointment_date, appointment_time)
            If True → return {'status': 'ERROR', 'message': 'DOUBLE BOOKING: ...'}

        Step 4: Create appointment
            Create Appointment object and call self.appt_repo.create()
            return {'status': 'SUCCESS', 'message': '...'}

        Step 5: Handle exceptions
            Wrap in try/except, return ERROR on failure

        Returns:
            dict with 'status' ('SUCCESS' or 'ERROR') and 'message'
        """
        # TODO: Implement all 5 steps above
        return {
            'status': 'ERROR',
            'message': 'Not yet implemented'
        }

    def schedule_via_procedure(
        self,
        appointment_id: str,
        doctor_id: str,
        patient_id: str,
        appointment_date: date,
        appointment_time: time
    ) -> dict:
        """
        Schedule via stored procedure sp_schedule_appointment.

        TODO: Use cursor.callproc('sp_schedule_appointment', args)
        HINT: args = [appointment_id, doctor_id, patient_id, date, time, '', '']
              result = cursor.callproc(..., args)
              status = result[5], message = result[6]
        """
        # TODO: Implement
        return {'status': 'ERROR', 'message': 'Not yet implemented'}

    def cancel_appointment(self, appointment_id: str) -> dict:
        """
        Cancel an appointment.

        TODO: Check if appointment exists, then delete it
        """
        # TODO: Implement
        return {'status': 'ERROR', 'message': 'Not yet implemented'}

    def get_daily_appointments(self, target_date: date = None) -> list:
        """
        Get all appointments for a given date.

        TODO: If target_date is None, use date.today()
        TODO: Call self.appt_repo.get_by_date(target_date)
        """
        # TODO: Implement
        return []

    def get_patient_appointments(self, patient_id: str) -> list:
        """TODO: Call self.appt_repo.get_by_patient(patient_id)"""
        # TODO: Implement
        return []

    def get_doctor_appointments(self, doctor_id: str) -> list:
        """TODO: Call self.appt_repo.get_by_doctor(doctor_id)"""
        # TODO: Implement
        return []

    def get_all_appointments(self) -> list:
        """TODO: Call self.appt_repo.get_all()"""
        # TODO: Implement
        return []
