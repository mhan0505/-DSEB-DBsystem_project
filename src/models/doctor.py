"""Doctor model - Data class for Doctor entity."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Doctor:
    """Represents a doctor in the hospital system."""

    doctor_id: str
    doctor_name: str
    department_id: str
    specialty: Optional[str] = None

    def to_dict(self) -> dict:
        """
        Convert Doctor to dictionary.

        TODO: Return dict with keys: DoctorID, DoctorName, DepartmentID, Specialty
        """
        # TODO: Implement
        return {}

    @classmethod
    def from_dict(cls, data: dict) -> 'Doctor':
        """
        Create Doctor from database row dict.

        TODO: return cls(doctor_id=data['DoctorID'], ...)
        """
        # TODO: Implement
        pass

    def __str__(self):
        return f"[{self.doctor_id}] {self.doctor_name} - {self.specialty}"
