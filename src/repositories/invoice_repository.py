"""
Invoice Repository - CRUD operations for Invoices table.
"""

from src.database_connection import DatabaseConnection
from src.models.invoice import Invoice


class InvoiceRepository:
    """Data access layer for Invoice entity."""

    def __init__(self):
        self.db = DatabaseConnection()

    def get_all(self) -> list:
        """
        Get all invoices with patient info.

        TODO: SELECT with JOIN to Patients
        HINT: SELECT i.*, p.PatientName FROM Invoices i
              JOIN Patients p ON i.PatientID = p.PatientID
        """
        # TODO: Implement
        return []

    def get_by_id(self, invoice_id: str) -> dict:
        """TODO: SELECT WHERE InvoiceID = %s, JOIN Patients"""
        # TODO: Implement
        return None

    def get_by_patient(self, patient_id: str) -> list:
        """TODO: SELECT WHERE PatientID = %s ORDER BY InvoiceDate DESC"""
        # TODO: Implement
        return []

    def get_by_date_range(self, start_date, end_date) -> list:
        """
        Get invoices within a date range.

        TODO: SELECT WHERE InvoiceDate BETWEEN %s AND %s
        """
        # TODO: Implement
        return []

    def create(self, invoice: Invoice) -> bool:
        """TODO: INSERT INTO Invoices VALUES (...)"""
        # TODO: Implement
        return False

    def update(self, invoice: Invoice) -> bool:
        """TODO: UPDATE Invoices SET ... WHERE InvoiceID = %s"""
        # TODO: Implement
        return False

    def delete(self, invoice_id: str) -> bool:
        """TODO: DELETE FROM Invoices WHERE InvoiceID = %s"""
        # TODO: Implement
        return False

    def get_total_revenue(self) -> float:
        """
        Get total revenue from all invoices.

        TODO: SELECT COALESCE(SUM(TotalAmount), 0) FROM Invoices
        """
        # TODO: Implement
        return 0.0

    def count(self) -> int:
        """TODO: SELECT COUNT(*)"""
        # TODO: Implement
        return 0
