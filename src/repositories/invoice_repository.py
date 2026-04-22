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
        query = """
            SELECT i.InvoiceID, i.PatientID, i.InvoiceDate, i.TotalAmount,
                   p.PatientName, p.PhoneNumber
            FROM Invoices i
            JOIN Patients p ON i.PatientID = p.PatientID
            ORDER BY i.InvoiceDate DESC, i.InvoiceID
        """
        return self.db.execute_query(query)

    def get_by_id(self, invoice_id: str) -> dict:
        """TODO: SELECT WHERE InvoiceID = %s, JOIN Patients"""
        query = """
            SELECT i.*, p.PatientName, p.PhoneNumber, p.Address
            FROM Invoices i
            JOIN Patients p ON i.PatientID = p.PatientID
            WHERE i.InvoiceID = %s
        """
        results = self.db.execute_query(query, (invoice_id,))
        return results[0] if results else None

    def get_by_patient(self, patient_id: str) -> list:
        """TODO: SELECT WHERE PatientID = %s ORDER BY InvoiceDate DESC"""
        query = """
            SELECT * FROM Invoices
            WHERE PatientID = %s
            ORDER BY InvoiceDate DESC
        """
        return self.db.execute_query(query, (patient_id,))

    def get_by_date_range(self, start_date, end_date) -> list:
        """
        Get invoices within a date range.

        TODO: SELECT WHERE InvoiceDate BETWEEN %s AND %s
        """
        query = """
            SELECT i.*, p.PatientName
            FROM Invoices i
            JOIN Patients p ON i.PatientID = p.PatientID
            WHERE i.InvoiceDate BETWEEN %s AND %s
            ORDER BY i.InvoiceDate
        """
        return self.db.execute_query(query, (start_date, end_date))

    def create(self, invoice: Invoice) -> bool:
        """TODO: INSERT INTO Invoices VALUES (...)"""
        query = """
            INSERT INTO Invoices (InvoiceID, PatientID, InvoiceDate, TotalAmount)
            VALUES (%s, %s, %s, %s)
        """
        params = (
            invoice.invoice_id, invoice.patient_id,
            invoice.invoice_date, float(invoice.total_amount)
        )
        affected = self.db.execute_query(query, params, fetch=False)
        return affected > 0

    def update(self, invoice: Invoice) -> bool:
        """TODO: UPDATE Invoices SET ... WHERE InvoiceID = %s"""
        query = """
            UPDATE Invoices
            SET PatientID = %s, InvoiceDate = %s, TotalAmount = %s
            WHERE InvoiceID = %s
        """
        params = (
            invoice.patient_id, invoice.invoice_date,
            float(invoice.total_amount), invoice.invoice_id
        )
        affected = self.db.execute_query(query, params, fetch=False)
        return affected > 0

    def delete(self, invoice_id: str) -> bool:
        """TODO: DELETE FROM Invoices WHERE InvoiceID = %s"""
        query = "DELETE FROM Invoices WHERE InvoiceID = %s"
        affected = self.db.execute_query(query, (invoice_id,), fetch=False)
        return affected > 0

    def get_total_revenue(self) -> float:
        """
        Get total revenue from all invoices.

        TODO: SELECT COALESCE(SUM(TotalAmount), 0) FROM Invoices
        """
        query = "SELECT COALESCE(SUM(TotalAmount), 0) AS total FROM Invoices"
        result = self.db.execute_query(query)
        return float(result[0]['total']) if result else 0.0

    def count(self) -> int:
        """TODO: SELECT COUNT(*)"""
        query = "SELECT COUNT(*) AS total FROM Invoices"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
