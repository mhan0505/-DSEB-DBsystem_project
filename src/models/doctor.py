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
        return {
            'DoctorID': self.doctor_id,
            'DoctorName': self.doctor_name,
            'DepartmentID': self.department_id,
            'Specialty': self.specialty
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Doctor':
        """
        Create Doctor from database row dict.

        TODO: return cls(doctor_id=data['DoctorID'], ...)
        """
        return cls(
            doctor_id=data['DoctorID'],
            doctor_name=data['DoctorName'],
            department_id=data['DepartmentID'],
            specialty=data.get('Specialty')
        )

    def __str__(self):
        return f"[{self.doctor_id}] {self.doctor_name} - {self.specialty}"
