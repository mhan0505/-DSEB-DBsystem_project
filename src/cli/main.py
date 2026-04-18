"""
Main CLI Application - Hospital Management System.
Entry point for all operations.

CONCEPT: This file ties everything together.
Students should implement this LAST, after all repositories and services work.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from datetime import date, time
from src.database_connection import DatabaseConnection
from src.repositories.patient_repository import PatientRepository
from src.repositories.doctor_repository import DoctorRepository
from src.repositories.department_repository import DepartmentRepository
from src.repositories.appointment_repository import AppointmentRepository
from src.repositories.invoice_repository import InvoiceRepository
from src.services.appointment_service import AppointmentService
from src.services.invoice_service import InvoiceService
from src.models.patient import Patient
from src.models.doctor import Doctor
from src.models.department import Department
from src.cli.report_menu import ReportMenu


class HospitalCLI:
    """Main CLI interface for Hospital Management System."""

    def __init__(self):
        self.db = DatabaseConnection()
        self.patient_repo = PatientRepository()
        self.doctor_repo = DoctorRepository()
        self.dept_repo = DepartmentRepository()
        self.appt_repo = AppointmentRepository()
        self.invoice_repo = InvoiceRepository()
        self.appt_service = AppointmentService()
        self.invoice_service = InvoiceService()
        self.report_menu = ReportMenu()

    def display_header(self):
        """Display application header."""
        print("\n" + "=" * 60)
        print("    🏥 HOSPITAL MANAGEMENT SYSTEM v1.0")
        print("    NEU DATCOM Lab - Database Management System")
        print("=" * 60)

    def display_main_menu(self):
        """Display main menu options."""
        print("\n📋 MAIN MENU")
        print("-" * 40)
        print("  1. 👤 Patient Management")
        print("  2. 🩺 Doctor Management")
        print("  3. 🏢 Department Management")
        print("  4. 📅 Appointment Management")
        print("  5. 💰 Invoice Management")
        print("  6. 📊 Reports & Statistics")
        print("  0. 🚪 Exit")
        print("-" * 40)

    def display_crud_menu(self, entity_name: str):
        """Display CRUD submenu."""
        print(f"\n--- {entity_name} Management ---")
        print("  1. View All")
        print("  2. Search / Find by ID")
        print("  3. Create New")
        print("  4. Update")
        print("  5. Delete")
        print("  0. Back to Main Menu")

    # =========================================================
    # PATIENT MANAGEMENT
    # =========================================================
    def patient_menu(self):
        """Patient management submenu."""
        while True:
            self.display_crud_menu("👤 Patient")
            choice = input("\nSelect option: ").strip()

            if choice == '1':
                self._list_patients()
            elif choice == '2':
                self._find_patient()
            elif choice == '3':
                self._create_patient()
            elif choice == '4':
                self._update_patient()
            elif choice == '5':
                self._delete_patient()
            elif choice == '0':
                break

    def _list_patients(self):
        """
        TODO: Get all patients from repo and display in table format
        HINT: patients = self.patient_repo.get_all()
              for p in patients: print(f"{p.patient_id} {p.patient_name} ...")
        """
        patients = self.patient_repo.get_all()
        print(f"\n📋 Total Patients: {len(patients)}")
        print(f"{'ID':<10} {'Name':<25} {'DOB':<12} {'Gender':<8} {'Phone':<15}")
        print("-" * 70)
        for p in patients:
            print(f"{p.patient_id:<10} {p.patient_name:<25} {p.date_of_birth} {p.gender or '-':<8} {p.phone_number or '-':<15}")

    def _find_patient(self):
        """
        TODO: Ask for Patient ID, find by ID, display details
        HINT: pid = input("Enter Patient ID: ")
              patient = self.patient_repo.get_by_id(pid)
        """
        search = input("Enter Patient ID or Name: ").strip()
        if search.upper().startswith('P'):
            patient = self.patient_repo.get_by_id(search)
            if patient:
                print(f"\n{patient}")
                print(f"  Address: {patient.address}")
                print(f"  Phone:   {patient.phone_number}")
                print(f"  Age:     {patient.age}")
            else:
                print(f"❌ Patient {search} not found")
        else:
            results = self.patient_repo.search_by_name(search)
            print(f"\n🔍 Found {len(results)} patients matching '{search}':")
            for p in results:
                print(f"  {p}")

    def _create_patient(self):
        """
        TODO: Ask user for patient details, create Patient object, save to DB
        HINT: pid = input("Patient ID: ")
              name = input("Name: ")
              ...
              patient = Patient(pid, name, dob, gender, address, phone)
              self.patient_repo.create(patient)
        """
        print("\n--- Create New Patient ---")
        pid = input("Patient ID (e.g., P011): ").strip()
        name = input("Patient Name: ").strip()
        dob = input("Date of Birth (YYYY-MM-DD): ").strip()
        gender = input("Gender (M/F/O): ").strip().upper()
        address = input("Address: ").strip()
        phone = input("Phone Number: ").strip()
        try:
            patient = Patient(
                patient_id=pid, patient_name=name,
                date_of_birth=date.fromisoformat(dob),
                gender=gender if gender else None,
                address=address or None, phone_number=phone or None
            )
            if self.patient_repo.create(patient):
                print(f"✅ Patient {pid} created successfully!")
            else:
                print("❌ Failed to create patient")
        except Exception as e:
            print(f"❌ Error: {e}")

    def _update_patient(self):
        """
        TODO: Find existing patient, ask for new values, update in DB
        """
        pid = input("Enter Patient ID to update: ").strip()
        patient = self.patient_repo.get_by_id(pid)
        if not patient:
            print(f"❌ Patient {pid} not found")
            return
        print(f"\nCurrent: {patient}")
        name = input(f"New name [{patient.patient_name}]: ").strip() or patient.patient_name
        phone = input(f"New phone [{patient.phone_number}]: ").strip() or patient.phone_number
        address = input(f"New address [{patient.address}]: ").strip() or patient.address
        patient.patient_name = name
        patient.phone_number = phone
        patient.address = address
        if self.patient_repo.update(patient):
            print(f"✅ Patient {pid} updated successfully!")
        else:
            print("❌ Failed to update patient")

    def _delete_patient(self):
        """
        TODO: Ask for Patient ID, confirm, then delete
        HINT: Handle FK constraint errors (patient may have appointments)
        """
        pid = input("Enter Patient ID to delete: ").strip()
        confirm = input(f"⚠️ Delete patient {pid}? (y/n): ").strip().lower()
        if confirm == 'y':
            try:
                if self.patient_repo.delete(pid):
                    print(f"✅ Patient {pid} deleted")
                else:
                    print(f"❌ Patient {pid} not found")
            except Exception as e:
                print(f"❌ Cannot delete: {e}")
                print("  → Patient may have existing appointments or invoices")

    # =========================================================
    # DOCTOR & DEPARTMENT MANAGEMENT
    # =========================================================
    def doctor_menu(self):
        """Doctor management submenu."""
        while True:
            self.display_crud_menu("🩺 Doctor")
            choice = input("\nSelect option: ").strip()
            if choice == '1':
                doctors = self.doctor_repo.get_all()
                print(f"\n📋 Total Doctors: {len(doctors)}")
                print(f"{'ID':<10} {'Name':<25} {'Department':<20} {'Specialty':<25}")
                print("-" * 80)
                for d in doctors:
                    print(f"{d['DoctorID']:<10} {d['DoctorName']:<25} {d['DepartmentName']:<20} {d.get('Specialty', '-'):<25}")
            elif choice == '2':
                did = input("Enter Doctor ID: ").strip()
                doctor = self.doctor_repo.get_by_id(did)
                print(f"\n{doctor}" if doctor else f"❌ Doctor {did} not found")
            elif choice == '3':
                print("\n--- Create New Doctor ---")
                did = input("Doctor ID (e.g., DR009): ").strip()
                name = input("Doctor Name: ").strip()
                dept_id = input("Department ID: ").strip()
                specialty = input("Specialty: ").strip()
                try:
                    doctor = Doctor(doctor_id=did, doctor_name=name, department_id=dept_id, specialty=specialty or None)
                    if self.doctor_repo.create(doctor):
                        print(f"✅ Doctor {did} created successfully!")
                    else:
                        print("❌ Failed to create doctor")
                except Exception as e:
                    print(f"❌ Error: {e}")
            elif choice == '4':
                did = input("Enter Doctor ID to update: ").strip()
                doctor = self.doctor_repo.get_by_id(did)
                if not doctor:
                    print(f"❌ Doctor {did} not found")
                    continue
                name = input(f"New name [{doctor.doctor_name}]: ").strip() or doctor.doctor_name
                specialty = input(f"New specialty [{doctor.specialty}]: ").strip() or doctor.specialty
                doctor.doctor_name = name
                doctor.specialty = specialty
                if self.doctor_repo.update(doctor):
                    print(f"✅ Doctor {did} updated!")
                else:
                    print("❌ Update failed")
            elif choice == '5':
                did = input("Enter Doctor ID to delete: ").strip()
                confirm = input(f"⚠️ Delete doctor {did}? (y/n): ").strip().lower()
                if confirm == 'y':
                    try:
                        if self.doctor_repo.delete(did):
                            print(f"✅ Doctor {did} deleted")
                        else:
                            print(f"❌ Doctor {did} not found")
                    except Exception as e:
                        print(f"❌ Cannot delete: {e}")
            elif choice == '0':
                break

    def department_menu(self):
        """Department management submenu."""
        while True:
            self.display_crud_menu("🏢 Department")
            choice = input("\nSelect option: ").strip()
            if choice == '1':
                depts = self.dept_repo.get_all()
                print(f"\n📋 Departments ({len(depts)}):")
                for d in depts:
                    print(f"  {d}")
            elif choice == '2':
                did = input("Department ID: ").strip()
                dept = self.dept_repo.get_by_id(did)
                print(f"\n{dept}" if dept else "❌ Not found")
            elif choice == '3':
                did = input("Department ID (e.g., D007): ").strip()
                name = input("Department Name: ").strip()
                dept = Department(department_id=did, department_name=name)
                if self.dept_repo.create(dept):
                    print(f"✅ Department {did} created!")
            elif choice == '4':
                did = input("Department ID to update: ").strip()
                name = input("New name: ").strip()
                dept = Department(department_id=did, department_name=name)
                if self.dept_repo.update(dept):
                    print("✅ Updated!")
            elif choice == '5':
                did = input("Department ID to delete: ").strip()
                try:
                    if self.dept_repo.delete(did):
                        print("✅ Deleted")
                except Exception as e:
                    print(f"❌ Error: {e}")
            elif choice == '0':
                break

    # =========================================================
    # ⭐ APPOINTMENT MANAGEMENT (CORE BUSINESS LOGIC)
    # =========================================================
    def appointment_menu(self):
        """Appointment management submenu."""
        while True:
            print("\n--- 📅 Appointment Management ---")
            print("  1. View All Appointments")
            print("  2. View Daily Appointments")
            print("  3. ⭐ Schedule New Appointment")
            print("  4. Cancel Appointment")
            print("  5. Find by Patient ID")
            print("  0. Back")

            choice = input("\nSelect option: ").strip()

            if choice == '1':
                appointments = self.appt_service.get_all_appointments()
                print(f"\n📋 Total Appointments: {len(appointments)}")
                print(f"{'ID':<8} {'Date':<12} {'Time':<10} {'Doctor':<25} {'Patient':<20}")
                print("-" * 75)
                for a in appointments:
                    print(f"{a['AppointmentID']:<8} {a['AppointmentDate']} {str(a['AppointmentTime']):<10} "
                          f"{a['DoctorName']:<25} {a['PatientName']:<20}")
            elif choice == '2':
                date_str = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
                target = date.fromisoformat(date_str) if date_str else date.today()
                appointments = self.appt_service.get_daily_appointments(target)
                print(f"\n📅 Appointments on {target}: {len(appointments)}")
                for a in appointments:
                    print(f"  {a['AppointmentTime']} - {a['DoctorName']} → {a['PatientName']} ({a['PhoneNumber']})")
            elif choice == '3':
                self._schedule_appointment()
            elif choice == '4':
                aid = input("Appointment ID to cancel: ").strip()
                result = self.appt_service.cancel_appointment(aid)
                icon = "✅" if result['status'] == 'SUCCESS' else "❌"
                print(f"{icon} {result['message']}")
            elif choice == '5':
                pid = input("Patient ID: ").strip()
                appointments = self.appt_service.get_patient_appointments(pid)
                print(f"\n📋 Appointments for {pid}: {len(appointments)}")
                for a in appointments:
                    print(f"  [{a['AppointmentID']}] {a['AppointmentDate']} {a['AppointmentTime']} "
                          f"- {a['DoctorName']} ({a['Specialty']})")
            elif choice == '0':
                break

    def _schedule_appointment(self):
        """
        ⭐ Schedule appointment with double booking prevention.

        TODO: Implement these steps:
        1. Ask user for: appointment_id, doctor_id, patient_id, date, time
        2. Parse date and time from strings
        3. Call self.appt_service.schedule_appointment(...)
        4. Display the result (SUCCESS or ERROR with message)
        """
        print("\n--- ⭐ Schedule New Appointment ---")
        print("  (System will check for double booking)")

        aid = input("Appointment ID (e.g., A011): ").strip()
        did = input("Doctor ID: ").strip()
        pid = input("Patient ID: ").strip()
        date_str = input("Date (YYYY-MM-DD): ").strip()
        time_str = input("Time (HH:MM:SS): ").strip()
        try:
            appt_date = date.fromisoformat(date_str)
            parts = time_str.split(':')
            appt_time = time(int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) > 2 else 0)
            result = self.appt_service.schedule_appointment(aid, did, pid, appt_date, appt_time)
            icon = "✅" if result['status'] == 'SUCCESS' else "❌"
            print(f"\n{icon} [{result['status']}] {result['message']}")
        except ValueError as e:
            print(f"❌ Invalid input: {e}")

    # =========================================================
    # INVOICE MANAGEMENT
    # =========================================================
    def invoice_menu(self):
        """Invoice management submenu."""
        while True:
            print("\n--- 💰 Invoice Management ---")
            print("  1. View All Invoices")
            print("  2. Find Invoice by ID")
            print("  3. Create New Invoice")
            print("  4. Patient Invoice History")
            print("  5. Total Revenue")
            print("  0. Back")
            choice = input("\nSelect option: ").strip()
            if choice == '1':
                invoices = self.invoice_service.get_all_invoices()
                print(f"\n📋 Total Invoices: {len(invoices)}")
                print(f"{'ID':<10} {'Patient':<20} {'Date':<12} {'Amount':>15}")
                print("-" * 57)
                for inv in invoices:
                    print(f"{inv['InvoiceID']:<10} {inv['PatientName']:<20} "
                          f"{inv['InvoiceDate']} {inv['TotalAmount']:>15,.2f}")
            elif choice == '2':
                iid = input("Invoice ID: ").strip()
                inv = self.invoice_repo.get_by_id(iid)
                if inv:
                    print(f"\n📄 Invoice: {inv['InvoiceID']}")
                    print(f"  Patient:  {inv['PatientName']} ({inv['PatientID']})")
                    print(f"  Date:     {inv['InvoiceDate']}")
                    print(f"  Amount:   {inv['TotalAmount']:,.2f} VND")
                else:
                    print(f"❌ Invoice {iid} not found")
            elif choice == '3':
                iid = input("Invoice ID (e.g., INV009): ").strip()
                pid = input("Patient ID: ").strip()
                inv_date = input("Invoice Date (YYYY-MM-DD): ").strip()
                amount = input("Total Amount: ").strip()
                result = self.invoice_service.create_invoice(
                    iid, pid, date.fromisoformat(inv_date), float(amount)
                )
                icon = "✅" if result['status'] == 'SUCCESS' else "❌"
                print(f"{icon} {result['message']}")
            elif choice == '4':
                pid = input("Patient ID: ").strip()
                invoices = self.invoice_service.get_patient_invoices(pid)
                total = sum(float(i.get('TotalAmount', 0)) for i in invoices)
                print(f"\n📋 Invoices for {pid}: {len(invoices)}")
                for inv in invoices:
                    print(f"  [{inv['InvoiceID']}] {inv['InvoiceDate']} - {inv['TotalAmount']:,.2f} VND")
                print(f"\n  Total: {total:,.2f} VND")
            elif choice == '5':
                total = self.invoice_service.get_total_revenue()
                print(f"\n💰 Total Revenue: {total:,.2f} VND")
            elif choice == '0':
                break

    # =========================================================
    # MAIN LOOP
    # =========================================================
    def run(self):
        """Main application loop."""
        try:
            self.db.connect()
            self.display_header()

            while True:
                self.display_main_menu()
                choice = input("Select option: ").strip()

                if choice == '1':
                    self.patient_menu()
                elif choice == '2':
                    self.doctor_menu()
                elif choice == '3':
                    self.department_menu()
                elif choice == '4':
                    self.appointment_menu()
                elif choice == '5':
                    self.invoice_menu()
                elif choice == '6':
                    self.report_menu.show()
                elif choice == '0':
                    print("\n👋 Goodbye!")
                    break
                else:
                    print("❌ Invalid option.")

        except KeyboardInterrupt:
            print("\n\n👋 Terminated.")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        finally:
            self.db.disconnect()


def main():
    app = HospitalCLI()
    app.run()


if __name__ == '__main__':
    main()
