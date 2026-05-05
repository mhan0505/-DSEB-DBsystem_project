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
        date_str = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
        target_date = date.fromisoformat(date_str) if date_str else date.today()
        if target_date == date.today():
            query = """
                SELECT AppointmentTime, DoctorName, Specialty,
                       DepartmentName, PatientName, PhoneNumber
                FROM vw_daily_appointments
                ORDER BY AppointmentTime
            """
            results = self.db.execute_query(query)
        else:
            query = """
                SELECT a.AppointmentTime, d.DoctorName, d.Specialty,
                       dep.DepartmentName, p.PatientName, p.PhoneNumber
                FROM Appointments a
                JOIN Doctors d ON a.DoctorID = d.DoctorID
                JOIN Departments dep ON d.DepartmentID = dep.DepartmentID
                JOIN Patients p ON a.PatientID = p.PatientID
                WHERE a.AppointmentDate = %s
                ORDER BY a.AppointmentTime
            """
            results = self.db.execute_query(query, (target_date,))
        print(f"\n{'='*70}")
        print(f"  📅 DAILY APPOINTMENTS REPORT - {target_date}")
        print(f"  Total: {len(results)} appointment(s)")
        print(f"{'='*70}")
        if not results:
            print("  No appointments scheduled for this date.")
            return
        print(f"\n  {'Time':<10} {'Doctor':<22} {'Specialty':<20} {'Patient':<18}")
        print(f"  {'-'*70}")
        for r in results:
            print(f"  {str(r['AppointmentTime']):<10} {r['DoctorName']:<22} "
                  f"{r['Specialty']:<20} {r['PatientName']:<18}")

    def _doctor_performance_report(self):
        """
        ⭐ Report: Doctor performance (uses VIEW vw_doctor_appointments)
 hehehehehe
        TODO: Execute "SELECT * FROM vw_doctor_appointments"
        TODO: Display: ID | Doctor | Specialty | Department | Appointments
        """
        query = "SELECT * FROM vw_doctor_appointments"
        results = self.db.execute_query(query)
        print(f"\n{'='*70}")
        print(f"  🩺 DOCTOR PERFORMANCE REPORT")
        print(f"{'='*70}")
        print(f"\n  {'ID':<8} {'Doctor':<22} {'Specialty':<22} {'Dept':<15} {'Appts':>6}")
        print(f"  {'-'*73}")
        for r in results:
            print(f"  {r['DoctorID']:<8} {r['DoctorName']:<22} "
                  f"{r.get('Specialty', '-'):<22} {r['DepartmentName']:<15} "
                  f"{r['TotalAppointments']:>6}")

    def _patient_visit_report(self):
        """
        ⭐ Report: Patient visit history (uses VIEW vw_patient_visit_history)

        TODO: Execute "SELECT * FROM vw_patient_visit_history"
        TODO: Display: ID | Patient | Visits | First/Last Visit | Total Spent
        """
        query = "SELECT * FROM vw_patient_visit_history"
        results = self.db.execute_query(query)
        print(f"\n{'='*80}")
        print(f"  👤 PATIENT VISIT HISTORY REPORT")
        print(f"{'='*80}")
        print(f"\n  {'ID':<8} {'Patient':<22} {'Gender':<8} {'Visits':>6} {'First Visit':<12} {'Last Visit':<12} {'Total Spent':>14}")
        print(f"  {'-'*82}")
        for r in results:
            print(f"  {r['PatientID']:<8} {r['PatientName']:<22} {r.get('Gender', '-'):<8} "
                  f"{r['TotalVisits']:>6} {str(r.get('FirstVisit', '-')):<12} "
                  f"{str(r.get('LastVisit', '-')):<12} {float(r.get('TotalSpent', 0)):>14,.2f}")

    def _monthly_revenue_report(self):
        """
        ⭐ Report: Monthly revenue (uses VIEW vw_monthly_revenue)

        TODO: Call self.invoice_service.get_monthly_revenue()
        TODO: Display table with: Month | Invoices | Revenue | Average
        TODO: Calculate and show totals at the bottom
        """
        results = self.invoice_service.get_monthly_revenue()
        print(f"\n{'='*70}")
        print(f"  💰 MONTHLY REVENUE REPORT")
        print(f"{'='*70}")
        print(f"\n  {'Month':<12} {'Invoices':>10} {'Revenue':>16} {'Average':>14}")
        print(f"  {'-'*52}")
        total_revenue = 0
        total_invoices = 0
        for r in results:
            revenue = float(r.get('TotalRevenue', 0))
            avg = float(r.get('AvgInvoiceAmount', 0))
            total_revenue += revenue
            total_invoices += r.get('TotalInvoices', 0)
            print(f"  {r['YearMonth']:<12} {r['TotalInvoices']:>10} {revenue:>16,.2f} {avg:>14,.2f}")
        print(f"  {'-'*52}")
        print(f"  {'TOTAL':<12} {total_invoices:>10} {total_revenue:>16,.2f}")

    def _department_summary_report(self):
        """
        Report: Department summary

        TODO: Call self.invoice_service.get_department_revenue()
        TODO: Display: Department | Doctors | Appointments | Revenue
        """
        results = self.invoice_service.get_department_revenue()
        print(f"\n{'='*70}")
        print(f"  🏢 DEPARTMENT SUMMARY REPORT")
        print(f"{'='*70}")
        print(f"\n  {'ID':<8} {'Department':<20} {'Doctors':>8} {'Appts':>8} {'Revenue':>16}")
        print(f"  {'-'*60}")
        for r in results:
            revenue = float(r.get('TotalRevenue', 0))
            print(f"  {r['DepartmentID']:<8} {r['DepartmentName']:<20} "
                  f"{r['TotalDoctors']:>8} {r['TotalAppointments']:>8} {revenue:>16,.2f}")

    def _financial_summary(self):
        """
        TODO: Ask for start/end dates
        TODO: Get invoices in range
        TODO: Calculate total revenue, average, count
        TODO: Display summary
        """
        print("\n--- 📈 Financial Summary ---")
        start_str = input("Start date (YYYY-MM-DD): ").strip()
        end_str = input("End date   (YYYY-MM-DD): ").strip()
        try:
            start_date = date.fromisoformat(start_str)
            end_date = date.fromisoformat(end_str)
            summary = self.invoice_service.get_revenue_by_date_range(start_date, end_date)
            print(f"\n{'='*50}")
            print(f"  📈 FINANCIAL SUMMARY")
            print(f"  Period: {start_date} to {end_date}")
            print(f"{'='*50}")
            print(f"  Total Invoices: {summary['total_invoices']}")
            print(f"  Total Revenue:  {summary['total_revenue']:,.2f} VND")
            print(f"  Avg Invoice:    {summary['avg_invoice']:,.2f} VND")
        except ValueError as e:
            print(f"❌ Invalid date format: {e}")

    def _system_dashboard(self):
        """
        System overview - count records in each table.

        TODO: For each table, execute SELECT COUNT(*)
        TODO: Display: Patients: X, Doctors: X, etc.
        TODO: Show total revenue
        """
        queries = {
            'Patients': "SELECT COUNT(*) AS c FROM Patients",
            'Doctors': "SELECT COUNT(*) AS c FROM Doctors",
            'Departments': "SELECT COUNT(*) AS c FROM Departments",
            'Appointments': "SELECT COUNT(*) AS c FROM Appointments",
            'Invoices': "SELECT COUNT(*) AS c FROM Invoices",
        }
        print(f"\n{'='*50}")
        print(f"  📋 SYSTEM OVERVIEW DASHBOARD")
        print(f"  Date: {date.today()}")
        print(f"{'='*50}")
        for name, query in queries.items():
            result = self.db.execute_query(query)
            count = result[0]['c'] if result else 0
            print(f"  {name:<20} {count:>10} records")
        rev_result = self.db.execute_query("SELECT COALESCE(SUM(TotalAmount), 0) AS total FROM Invoices")
        total_rev = float(rev_result[0]['total']) if rev_result else 0
        print(f"\n  {'Total Revenue':<20} {total_rev:>10,.2f} VND")
        print(f"{'='*50}")
