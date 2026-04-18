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
        doctor = self.doctor_repo.get_by_id(doctor_id)
        if not doctor:
            return {'status': 'ERROR', 'message': f'Doctor {doctor_id} does not exist'}

        patient = self.patient_repo.get_by_id(patient_id)
        if not patient:
            return {'status': 'ERROR', 'message': f'Patient {patient_id} does not exist'}

        is_conflict = self.appt_repo.check_double_booking(doctor_id, appointment_date, appointment_time)
        if is_conflict:
            return {
                'status': 'ERROR',
                'message': (
                    f'DOUBLE BOOKING: Doctor {doctor_id} ({doctor.doctor_name}) '
                    f'already has an appointment on {appointment_date} at {appointment_time}'
                )
            }

        try:
            appointment = Appointment(
                appointment_id=appointment_id,
                doctor_id=doctor_id,
                patient_id=patient_id,
                appointment_date=appointment_date,
                appointment_time=appointment_time
            )
            success = self.appt_repo.create(appointment)
            if success:
                return {
                    'status': 'SUCCESS',
                    'message': (
                        f'Appointment {appointment_id} scheduled: '
                        f'{patient.patient_name} with {doctor.doctor_name} '
                        f'on {appointment_date} at {appointment_time}'
                    )
                }
            return {'status': 'ERROR', 'message': 'Failed to create appointment'}
        except Exception as e:
            return {'status': 'ERROR', 'message': f'Error scheduling appointment: {str(e)}'}

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
        try:
            cursor = self.db.get_cursor(dictionary=False)
            args = [appointment_id, doctor_id, patient_id, appointment_date, appointment_time, '', '']
            result = cursor.callproc('sp_schedule_appointment', args)
            self.db.commit()
            cursor.close()
            return {'status': result[5], 'message': result[6]}
        except Exception as e:
            return {'status': 'ERROR', 'message': f'Procedure error: {str(e)}'}

    def cancel_appointment(self, appointment_id: str) -> dict:
        """
        Cancel an appointment.

        TODO: Check if appointment exists, then delete it
        """
        existing = self.appt_repo.get_by_id(appointment_id)
        if not existing:
            return {'status': 'ERROR', 'message': f'Appointment {appointment_id} not found'}
        success = self.appt_repo.delete(appointment_id)
        if success:
            return {'status': 'SUCCESS', 'message': f'Appointment {appointment_id} cancelled successfully'}
        return {'status': 'ERROR', 'message': 'Failed to cancel appointment'}

    def get_daily_appointments(self, target_date: date = None) -> list:
        """
        Get all appointments for a given date.

        TODO: If target_date is None, use date.today()
        TODO: Call self.appt_repo.get_by_date(target_date)
        """
        if target_date is None:
            target_date = date.today()
        return self.appt_repo.get_by_date(target_date)

    def get_patient_appointments(self, patient_id: str) -> list:
        """TODO: Call self.appt_repo.get_by_patient(patient_id)"""
        return self.appt_repo.get_by_patient(patient_id)

    def get_doctor_appointments(self, doctor_id: str) -> list:
        """TODO: Call self.appt_repo.get_by_doctor(doctor_id)"""
        return self.appt_repo.get_by_doctor(doctor_id)

    def get_all_appointments(self) -> list:
        """TODO: Call self.appt_repo.get_all()"""
        return self.appt_repo.get_all()
