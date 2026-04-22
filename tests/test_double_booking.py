"""
⭐ TEST DOUBLE BOOKING - BUSINESS LOGIC CRITICAL

This test file verifies the most important business rule:
A doctor CANNOT have 2 patients at the same date and time.

HOW IT WORKS:
1. setUp: Create test data (test doctors + test patients)
2. Test: Try inserting conflicting appointments
3. tearDown: Clean up test data

IMPORTANT: This test requires a running MySQL database with hospital_db set up!
"""

import sys
import os
import unittest
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mysql.connector
from src.database_connection import DatabaseConnection


class TestDoubleBooking(unittest.TestCase):
    """Test suite for double booking prevention."""

    @classmethod
    def setUpClass(cls):
        """Connect to database once for all tests."""
        cls.db = DatabaseConnection()
        cls.db.connect()

    @classmethod
    def tearDownClass(cls):
        """Disconnect after all tests."""
        cls.db.disconnect()
        DatabaseConnection._instance = None

    def setUp(self):
        """Create fresh test data before each test."""
        self.slot_day_1 = (date.today() + timedelta(days=7)).isoformat()
        self.slot_day_2 = (date.today() + timedelta(days=8)).isoformat()
        self._cleanup()
        self._setup_test_data()

    def tearDown(self):
        """Remove test data after each test."""
        self._cleanup()

    def _cleanup(self):
        """Remove all test data (IDs starting with 'TEST')."""
        cursor = self.db.get_cursor(dictionary=False)
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("DELETE FROM Appointments WHERE AppointmentID LIKE 'TEST%'")
        cursor.execute("DELETE FROM Invoices WHERE PatientID LIKE 'TEST%'")
        cursor.execute("DELETE FROM Patients WHERE PatientID LIKE 'TEST%'")
        cursor.execute("DELETE FROM Doctors WHERE DoctorID LIKE 'TEST%'")
        cursor.execute("DELETE FROM Departments WHERE DepartmentID = 'TESTDEPT'")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        self.db.commit()
        cursor.close()

    def _setup_test_data(self):
        """
        TODO: Create test data:
        1. Insert a test department ('TESTDEPT')
        2. Insert 2 test doctors ('TEST_D01', 'TEST_D02')
        3. Insert 2 test patients ('TEST_P01', 'TEST_P02')
        """
        cursor = self.db.get_cursor(dictionary=False)

        cursor.execute("INSERT IGNORE INTO Departments (DepartmentID, DepartmentName) VALUES ('TESTDEPT', 'Test Department')")
        cursor.execute("INSERT INTO Doctors (DoctorID, DoctorName, DepartmentID, Specialty) VALUES ('TEST_D01', 'Dr. Test Alpha', 'TESTDEPT', 'Testing')")
        cursor.execute("INSERT INTO Doctors (DoctorID, DoctorName, DepartmentID, Specialty) VALUES ('TEST_D02', 'Dr. Test Beta', 'TESTDEPT', 'Testing')")
        cursor.execute("INSERT INTO Patients (PatientID, PatientName, DateOfBirth, Gender, Address, PhoneNumber) VALUES ('TEST_P01', 'Patient Alpha', '1990-01-01', 'M', 'Test Address 1', '0900000001')")
        cursor.execute("INSERT INTO Patients (PatientID, PatientName, DateOfBirth, Gender, Address, PhoneNumber) VALUES ('TEST_P02', 'Patient Beta', '1995-06-15', 'F', 'Test Address 2', '0900000002')")
        self.db.commit()
        cursor.close()

    def test_01_double_booking_prevented(self):
        """
        ⭐ MOST IMPORTANT TEST:
        Same doctor + Same date + Same time → MUST FAIL

        TODO: Implement:
        1. INSERT first appointment (should succeed)
        2. INSERT second appointment with SAME doctor, date, time (should FAIL)
        3. Use self.assertRaises(mysql.connector.errors.IntegrityError)
        4. Verify only 1 appointment exists for that slot
        """
        cursor = self.db.get_cursor(dictionary=False)
        cursor.execute("""
            INSERT INTO Appointments (AppointmentID, DoctorID, PatientID, AppointmentDate, AppointmentTime)
            VALUES ('TEST_A01', 'TEST_D01', 'TEST_P01', %s, '10:00:00')
        """, (self.slot_day_1,))
        self.db.commit()

        with self.assertRaises(mysql.connector.errors.IntegrityError) as context:
            cursor.execute("""
                INSERT INTO Appointments (AppointmentID, DoctorID, PatientID, AppointmentDate, AppointmentTime)
                VALUES ('TEST_A02', 'TEST_D01', 'TEST_P02', %s, '10:00:00')
            """, (self.slot_day_1,))
            self.db.commit()

        print(f"  ✅ Double booking correctly prevented! Error: {context.exception}")
        self.db.connection.rollback()
        cursor.execute("""
            SELECT COUNT(*) FROM Appointments
            WHERE DoctorID = 'TEST_D01' AND AppointmentDate = %s AND AppointmentTime = '10:00:00'
        """, (self.slot_day_1,))
        count = cursor.fetchone()[0]
        self.assertEqual(count, 1)
        cursor.close()

    def test_02_same_doctor_different_time_allowed(self):
        """
        Same doctor + Same date + DIFFERENT time → MUST SUCCEED

        TODO: Implement:
        1. INSERT appointment at 10:00
        2. INSERT appointment at 11:00 (different time)
        3. Verify both exist (count = 2)
        """
        cursor = self.db.get_cursor(dictionary=False)
        cursor.execute("INSERT INTO Appointments VALUES ('TEST_A03', 'TEST_D01', 'TEST_P01', %s, '10:00:00')", (self.slot_day_1,))
        cursor.execute("INSERT INTO Appointments VALUES ('TEST_A04', 'TEST_D01', 'TEST_P02', %s, '11:00:00')", (self.slot_day_1,))
        self.db.commit()
        cursor.execute("SELECT COUNT(*) FROM Appointments WHERE DoctorID = 'TEST_D01'")
        self.assertEqual(cursor.fetchone()[0], 2)
        print("  ✅ Same doctor, different time: correctly allowed")
        cursor.close()

    def test_03_different_doctor_same_time_allowed(self):
        """
        DIFFERENT doctor + Same date + Same time → MUST SUCCEED

        TODO: Implement:
        1. INSERT appointment for Doctor 1 at 10:00
        2. INSERT appointment for Doctor 2 at 10:00
        3. Verify both exist (count = 2)
        """
        cursor = self.db.get_cursor(dictionary=False)
        cursor.execute("INSERT INTO Appointments VALUES ('TEST_A05', 'TEST_D01', 'TEST_P01', %s, '10:00:00')", (self.slot_day_1,))
        cursor.execute("INSERT INTO Appointments VALUES ('TEST_A06', 'TEST_D02', 'TEST_P02', %s, '10:00:00')", (self.slot_day_1,))
        self.db.commit()
        cursor.execute("SELECT COUNT(*) FROM Appointments WHERE AppointmentDate = %s AND AppointmentTime = '10:00:00'", (self.slot_day_1,))
        self.assertEqual(cursor.fetchone()[0], 2)
        print("  ✅ Different doctor, same time: correctly allowed")
        cursor.close()

    def test_04_same_doctor_different_date_allowed(self):
        """
        Same doctor + DIFFERENT date + Same time → MUST SUCCEED

        TODO: Implement:
        1. INSERT appointment on June 15 at 10:00
        2. INSERT appointment on June 16 at 10:00
        3. Verify both exist
        """
        cursor = self.db.get_cursor(dictionary=False)
        cursor.execute("INSERT INTO Appointments VALUES ('TEST_A07', 'TEST_D01', 'TEST_P01', %s, '10:00:00')", (self.slot_day_1,))
        cursor.execute("INSERT INTO Appointments VALUES ('TEST_A08', 'TEST_D01', 'TEST_P02', %s, '10:00:00')", (self.slot_day_2,))
        self.db.commit()
        cursor.execute("SELECT COUNT(*) FROM Appointments WHERE DoctorID = 'TEST_D01'")
        self.assertEqual(cursor.fetchone()[0], 2)
        print("  ✅ Same doctor, different date: correctly allowed")
        cursor.close()


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  ⭐ DOUBLE BOOKING PREVENTION TESTS")
    print("=" * 60 + "\n")
    unittest.main(verbosity=2)
