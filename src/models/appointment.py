"""Appointment model - Data class for Appointment entity."""

from dataclasses import dataclass
from datetime import date, time


@dataclass
class Appointment:
    """Represents an appointment in the hospital system."""

    appointment_id: str
    doctor_id: str
    patient_id: str
    appointment_date: date
    appointment_time: time

    def to_dict(self) -> dict:
        """
        Convert Appointment to dictionary.

        TODO: Return dict with keys matching DB columns:
        AppointmentID, DoctorID, PatientID, AppointmentDate, AppointmentTime
        HINT: Use .isoformat() for date, str() for time
        """
        # TODO: Implement
        return {}

    @classmethod
    def from_dict(cls, data: dict) -> 'Appointment':
        """
        Create Appointment from database row dict.

        TODO: Handle type conversion for date and time fields.
        HINT: If data['AppointmentDate'] is a string, use date.fromisoformat()
        HINT: If data['AppointmentTime'] is a string, parse H:M:S
        """
        # TODO: Implement
        pass

    def __str__(self):
        return (f"[{self.appointment_id}] Dr:{self.doctor_id} - Patient:{self.patient_id} "
                f"on {self.appointment_date} at {self.appointment_time}")
