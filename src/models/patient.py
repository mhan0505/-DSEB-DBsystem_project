"""
Patient model - Data class for Patient entity.

CONCEPT: @dataclass automatically generates __init__, __repr__, __eq__
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Patient:
    """Represents a patient in the hospital system."""

    patient_id: str
    patient_name: str
    date_of_birth: date
    gender: Optional[str] = None        # M, F, O
    address: Optional[str] = None
    phone_number: Optional[str] = None

    def __post_init__(self):
        """Validate data after initialization."""
        if self.gender and self.gender not in ('M', 'F', 'O'):
            raise ValueError(f"Invalid gender: {self.gender}. Must be M, F, or O")

    @property
    def age(self) -> int:
        """
        Calculate current age from date_of_birth.

        TODO: Calculate age in years
        HINT: today.year - dob.year - adjustment_for_birthday_not_yet
        """
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def to_dict(self) -> dict:
        """
        Convert Patient to dictionary (for database operations).

        TODO: Return a dict with keys matching database column names:
        {'PatientID': ..., 'PatientName': ..., 'DateOfBirth': ...,
         'Gender': ..., 'Address': ..., 'PhoneNumber': ...}
        """
        return {
            'PatientID': self.patient_id,
            'PatientName': self.patient_name,
            'DateOfBirth': self.date_of_birth.isoformat(),
            'Gender': self.gender,
            'Address': self.address,
            'PhoneNumber': self.phone_number
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Patient':
        """
        Create Patient from a database row (dictionary).

        TODO: Extract values from data dict and create Patient instance.
        HINT: Handle DateOfBirth conversion (str → date if needed)
        """
        dob = data['DateOfBirth']
        if isinstance(dob, str):
            dob = date.fromisoformat(dob)
        return cls(
            patient_id=data['PatientID'],
            patient_name=data['PatientName'],
            date_of_birth=dob,
            gender=data.get('Gender'),
            address=data.get('Address'),
            phone_number=data.get('PhoneNumber')
        )

    def __str__(self):
        return f"[{self.patient_id}] {self.patient_name}"
