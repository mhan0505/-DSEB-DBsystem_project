"""
Report Menu - Business Reports & Statistics.
⭐ Theo yêu cầu đề bài: "Patient visits" + "Financial transactions"
"""

from datetime import date
from src.database_connection import DatabaseConnection
from src.services.invoice_service import InvoiceService


class ReportMenu:
    """Reports and statistics menu."""

    def __init__(self):
        self.db = DatabaseConnection()
        self.invoice_service = InvoiceService()

    def show(self):
        """Display reports menu."""
        while True:
            print("\n" + "=" * 50)
            print("  📊 REPORTS & STATISTICS")
            print("=" * 50)
            print("  1. 📅 Daily Appointments Report")
            print("  2. 🩺 Doctor Performance Report")
            print("  3. 👤 Patient Visit History Report")
            print("  4. 💰 Monthly Revenue Report")
            print("  5. 🏢 Department Summary Report")
            print("  6. 📈 Financial Summary (Date Range)")
            print("  7. 📋 System Overview Dashboard")
            print("  0. ← Back")

            choice = input("Select report: ").strip()

            if choice == '1':
                self._daily_appointments_report()
            elif choice == '2':
                self._doctor_performance_report()
            elif choice == '3':
                self._patient_visit_report()
            elif choice == '4':
                self._monthly_revenue_report()
            elif choice == '5':
                self._department_summary_report()
            elif choice == '6':
                self._financial_summary()
            elif choice == '7':
                self._system_dashboard()
            elif choice == '0':
                break

    def _daily_appointments_report(self):
        """
        ⭐ Report: Daily appointments

        TODO: Ask for date (or use today)
        TODO: Query appointments for that date (JOIN Doctors, Patients)
        TODO: Display in table format: Time | Doctor | Specialty | Patient
        """
        # TODO: Implement
        print("TODO: Daily appointments report")

    def _doctor_performance_report(self):
        """
        ⭐ Report: Doctor performance (uses VIEW vw_doctor_appointments)
 hehehehehe
        TODO: Execute "SELECT * FROM vw_doctor_appointments"
        TODO: Display: ID | Doctor | Specialty | Department | Appointments
        """
        # TODO: Implement
        print("TODO: Doctor performance report")

    def _patient_visit_report(self):
        """
        ⭐ Report: Patient visit history (uses VIEW vw_patient_visit_history)

        TODO: Execute "SELECT * FROM vw_patient_visit_history"
        TODO: Display: ID | Patient | Visits | First/Last Visit | Total Spent
        """
        # TODO: Implement
        print("TODO: Patient visit history report")

    def _monthly_revenue_report(self):
        """
        ⭐ Report: Monthly revenue (uses VIEW vw_monthly_revenue)

        TODO: Call self.invoice_service.get_monthly_revenue()
        TODO: Display table with: Month | Invoices | Revenue | Average
        TODO: Calculate and show totals at the bottom
        """
        # TODO: Implement
        print("TODO: Monthly revenue report")

    def _department_summary_report(self):
        """
        Report: Department summary

        TODO: Call self.invoice_service.get_department_revenue()
        TODO: Display: Department | Doctors | Appointments | Revenue
        """
        # TODO: Implement
        print("TODO: Department summary report")

    def _financial_summary(self):
        """
        TODO: Ask for start/end dates
        TODO: Get invoices in range
        TODO: Calculate total revenue, average, count
        TODO: Display summary
        """
        # TODO: Implement
        print("TODO: Financial summary")

    def _system_dashboard(self):
        """
        System overview - count records in each table.

        TODO: For each table, execute SELECT COUNT(*)
        TODO: Display: Patients: X, Doctors: X, etc.
        TODO: Show total revenue
        """
        # TODO: Implement
        print("TODO: System dashboard")
