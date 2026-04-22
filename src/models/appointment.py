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
        return {
            'AppointmentID': self.appointment_id,
            'DoctorID': self.doctor_id,
            'PatientID': self.patient_id,
            'AppointmentDate': self.appointment_date.isoformat(),
            'AppointmentTime': str(self.appointment_time)
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Appointment':
        """
        Create Appointment from database row dict.

        TODO: Handle type conversion for date and time fields.
        HINT: If data['AppointmentDate'] is a string, use date.fromisoformat()
        HINT: If data['AppointmentTime'] is a string, parse H:M:S
        """
        appt_date = data['AppointmentDate']
        appt_time = data['AppointmentTime']
        if isinstance(appt_date, str):
            appt_date = date.fromisoformat(appt_date)
        if isinstance(appt_time, str):
            parts = appt_time.split(':')
            appt_time = time(int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) > 2 else 0)
        return cls(
            appointment_id=data['AppointmentID'],
            doctor_id=data['DoctorID'],
            patient_id=data['PatientID'],
            appointment_date=appt_date,
            appointment_time=appt_time
        )

    def __str__(self):
        return (f"[{self.appointment_id}] Dr:{self.doctor_id} - Patient:{self.patient_id} "
                f"on {self.appointment_date} at {self.appointment_time}")
