"""Department model - Data class for Department entity."""

from dataclasses import dataclass


@dataclass
class Department:
    """Represents a department in the hospital."""

    department_id: str
    department_name: str

    def to_dict(self) -> dict:
        """
        Convert Department to dictionary.

        TODO: Return dict with keys: DepartmentID, DepartmentName
        """
        # TODO: Implement
        return {}

    @classmethod
    def from_dict(cls, data: dict) -> 'Department':
        """
        Create Department from database row dict.

        TODO: return cls(department_id=data['DepartmentID'], ...)
        """
        # TODO: Implement
        pass

    def __str__(self):
        return f"[{self.department_id}] {self.department_name}"
