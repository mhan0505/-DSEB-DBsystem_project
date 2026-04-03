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

    # =========================================================
    # PATIENT MANAGEMENT
    # =========================================================
    def patient_menu(self):
        """Patient management submenu."""
        while True:
            print("\n--- 👤 Patient Management ---")
            print("  1. View All Patients")
            print("  2. Search / Find by ID")
            print("  3. Create New Patient")
            print("  4. Update Patient")
            print("  5. Delete Patient")
            print("  0. Back")

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
        # TODO: Implement
        print("TODO: List all patients")

    def _find_patient(self):
        """
        TODO: Ask for Patient ID, find by ID, display details
        HINT: pid = input("Enter Patient ID: ")
              patient = self.patient_repo.get_by_id(pid)
        """
        # TODO: Implement
        print("TODO: Find patient")

    def _create_patient(self):
        """
        TODO: Ask user for patient details, create Patient object, save to DB
        HINT: pid = input("Patient ID: ")
              name = input("Name: ")
              ...
              patient = Patient(pid, name, dob, gender, address, phone)
              self.patient_repo.create(patient)
        """
        # TODO: Implement
        print("TODO: Create patient")

    def _update_patient(self):
        """
        TODO: Find existing patient, ask for new values, update in DB
        """
        # TODO: Implement
        print("TODO: Update patient")

    def _delete_patient(self):
        """
        TODO: Ask for Patient ID, confirm, then delete
        HINT: Handle FK constraint errors (patient may have appointments)
        """
        # TODO: Implement
        print("TODO: Delete patient")

    # =========================================================
    # DOCTOR & DEPARTMENT MANAGEMENT
    # =========================================================
    def doctor_menu(self):
        """
        TODO: Similar to patient_menu but for Doctors
        - View all, Find, Create, Update, Delete
        """
        # TODO: Implement (similar pattern to patient_menu)
        print("TODO: Doctor management menu")

    def department_menu(self):
        """
        TODO: Similar to patient_menu but for Departments
        - View all, Find, Create, Update, Delete
        """
        # TODO: Implement
        print("TODO: Department management menu")

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
                # TODO: Get and display all appointments
                print("TODO: List all appointments")
            elif choice == '2':
                # TODO: Ask for date, show appointments for that date
                print("TODO: Daily appointments")
            elif choice == '3':
                self._schedule_appointment()
            elif choice == '4':
                # TODO: Ask for appointment ID, cancel via service
                print("TODO: Cancel appointment")
            elif choice == '5':
                # TODO: Ask for patient ID, show their appointments
                print("TODO: Patient appointments")
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

        # TODO: Get user input
        # TODO: Call appt_service.schedule_appointment()
        # TODO: Display result
        print("TODO: Schedule appointment")

    # =========================================================
    # INVOICE MANAGEMENT
    # =========================================================
    def invoice_menu(self):
        """
        TODO: Invoice management submenu
        - View all, Find by ID, Create, Patient history, Total revenue
        """
        # TODO: Implement
        print("TODO: Invoice management menu")

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
