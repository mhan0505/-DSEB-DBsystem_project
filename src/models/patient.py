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
        # TODO: Validate that gender is one of 'M', 'F', 'O' (or None)
        # HINT: if self.gender and self.gender not in ('M', 'F', 'O'):
        #           raise ValueError(...)
        pass

    @property
    def age(self) -> int:
        """
        Calculate current age from date_of_birth.

        TODO: Calculate age in years
        HINT: today.year - dob.year - adjustment_for_birthday_not_yet
        """
        # TODO: Implement age calculation
        return 0

    def to_dict(self) -> dict:
        """
        Convert Patient to dictionary (for database operations).

        TODO: Return a dict with keys matching database column names:
        {'PatientID': ..., 'PatientName': ..., 'DateOfBirth': ...,
         'Gender': ..., 'Address': ..., 'PhoneNumber': ...}
        """
        # TODO: Implement to_dict
        return {}

    @classmethod
    def from_dict(cls, data: dict) -> 'Patient':
        """
        Create Patient from a database row (dictionary).

        TODO: Extract values from data dict and create Patient instance.
        HINT: Handle DateOfBirth conversion (str → date if needed)
        """
        # TODO: Implement from_dict
        # HINT: return cls(patient_id=data['PatientID'], ...)
        pass

    def __str__(self):
        return f"[{self.patient_id}] {self.patient_name}"
