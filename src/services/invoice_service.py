"""
Invoice Service - Business Logic Layer.
⭐ Invoice calculation and financial reports.
"""

from datetime import date
from decimal import Decimal
from src.database_connection import DatabaseConnection
from src.repositories.invoice_repository import InvoiceRepository
from src.models.invoice import Invoice
from src.config import CONSULTATION_FEE


class InvoiceService:
    """Business logic for invoice management."""

    def __init__(self):
        self.invoice_repo = InvoiceRepository()
        self.db = DatabaseConnection()

    def create_invoice(self, invoice_id, patient_id, invoice_date, total_amount) -> dict:
        """
        Create a new invoice with validation.

        TODO: Validate total_amount >= 0
        TODO: Create Invoice object
        TODO: Call self.invoice_repo.create()
        TODO: Return status dict
        """
        if total_amount < 0:
            return {'status': 'ERROR', 'message': 'Total amount cannot be negative'}
        try:
            invoice = Invoice(
                invoice_id=invoice_id,
                patient_id=patient_id,
                invoice_date=invoice_date,
                total_amount=Decimal(str(total_amount))
            )
            success = self.invoice_repo.create(invoice)
            if success:
                return {'status': 'SUCCESS', 'message': f'Invoice {invoice_id} created: {total_amount:,.2f} VND'}
            return {'status': 'ERROR', 'message': 'Failed to create invoice'}
        except Exception as e:
            return {'status': 'ERROR', 'message': f'Error creating invoice: {str(e)}'}

    def calculate_invoice_total(self, patient_id: str, invoice_date: date) -> float:
        """
        ⭐ Calculate invoice total using UDF fn_calculate_invoice_total.

        TODO: Execute SQL: "SELECT fn_calculate_invoice_total(%s, %s) AS Total"
        TODO: Return the result as float
        """
        try:
            query = "SELECT fn_calculate_invoice_total(%s, %s) AS Total"
            results = self.db.execute_query(query, (patient_id, invoice_date))
            if results:
                return float(results[0]['Total'])
            return 0.0
        except Exception:
            return float(CONSULTATION_FEE)

    def get_monthly_revenue(self) -> list:
        """
        ⭐ Get monthly revenue report using VIEW vw_monthly_revenue.

        TODO: Execute "SELECT * FROM vw_monthly_revenue"
        """
        query = "SELECT * FROM vw_monthly_revenue"
        return self.db.execute_query(query)

    def get_patient_invoices(self, patient_id: str) -> list:
        """TODO: Call self.invoice_repo.get_by_patient(patient_id)"""
        return self.invoice_repo.get_by_patient(patient_id)

    def get_revenue_by_date_range(self, start_date, end_date) -> dict:
        """
        Get revenue summary for a date range.

        TODO: Get invoices from repo
        TODO: Calculate total_revenue, avg_invoice
        TODO: Return summary dict
        """
        invoices = self.invoice_repo.get_by_date_range(start_date, end_date)
        total_revenue = sum(float(inv.get('TotalAmount', 0)) for inv in invoices)
        return {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'total_invoices': len(invoices),
            'total_revenue': total_revenue,
            'avg_invoice': total_revenue / len(invoices) if invoices else 0,
            'invoices': invoices
        }

    def get_department_revenue(self) -> list:
        """TODO: SELECT * FROM vw_department_summary"""
        query = "SELECT * FROM vw_department_summary"
        return self.db.execute_query(query)

    def get_all_invoices(self) -> list:
        """TODO: Call self.invoice_repo.get_all()"""
        return self.invoice_repo.get_all()

    def get_total_revenue(self) -> float:
        """TODO: Call self.invoice_repo.get_total_revenue()"""
        return self.invoice_repo.get_total_revenue()
