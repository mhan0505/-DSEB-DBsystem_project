"""
⭐ TEST TRIGGERS - Auto Invoice Generation

Verifies: trg_after_appointment_insert trigger auto-creates invoices.
"""

import sys, os, unittest
from datetime import date, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database_connection import DatabaseConnection


class TestTriggers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = DatabaseConnection()
        cls.db.connect()

    @classmethod
    def tearDownClass(cls):
        cls.db.disconnect()
        DatabaseConnection._instance = None

    def setUp(self):
        self.trigger_day_1 = (date.today() + timedelta(days=7)).isoformat()
        self.trigger_day_2 = (date.today() + timedelta(days=8)).isoformat()
        self._cleanup()
        self._setup()

    def tearDown(self):
        self._cleanup()

    def _cleanup(self):
        c = self.db.get_cursor(dictionary=False)
        c.execute("SET FOREIGN_KEY_CHECKS = 0")
        c.execute("DELETE FROM Appointments WHERE AppointmentID LIKE 'TTRG%'")
        c.execute("DELETE FROM Invoices WHERE PatientID LIKE 'TTRG%'")
        c.execute("DELETE FROM Patients WHERE PatientID LIKE 'TTRG%'")
        c.execute("DELETE FROM Doctors WHERE DoctorID LIKE 'TTRG%'")
        c.execute("DELETE FROM Departments WHERE DepartmentID = 'TTRGDPT'")
        c.execute("SET FOREIGN_KEY_CHECKS = 1")
        self.db.commit(); c.close()

    def _setup(self):
        c = self.db.get_cursor(dictionary=False)
        c.execute("INSERT IGNORE INTO Departments VALUES ('TTRGDPT', 'Trigger Test Dept')")
        c.execute("INSERT INTO Doctors VALUES ('TTRG_D01', 'Dr. Trigger Test', 'TTRGDPT', 'Testing')")
        c.execute("INSERT INTO Patients VALUES ('TTRG_P01', 'Trigger Patient 1', '1990-01-01', 'M', 'Ha Noi', '0900000001')")
        c.execute("INSERT INTO Patients VALUES ('TTRG_P02', 'Trigger Patient 2', '1995-05-05', 'F', 'HCMC', '0900000002')")
        self.db.commit(); c.close()

    def test_trigger_creates_invoice(self):
        """
        ⭐ Insert appointment → Invoice should be auto-created by trigger

        TODO:
        1. Check no invoices exist for test patient (COUNT = 0)
        2. INSERT an appointment
        3. Check invoices again (COUNT should be >= 1)
        4. Verify invoice amount = 50,000
        """
        cursor = self.db.get_cursor(dictionary=False)
        cursor.execute("SELECT COUNT(*) FROM Invoices WHERE PatientID = 'TTRG_P01'")
        self.assertEqual(cursor.fetchone()[0], 0)

        cursor.execute("INSERT INTO Appointments (AppointmentID, DoctorID, PatientID, AppointmentDate, AppointmentTime) VALUES ('TTRG_A01', 'TTRG_D01', 'TTRG_P01', %s, '10:00:00')", (self.trigger_day_1,))
        self.db.commit()

        cursor.execute("SELECT COUNT(*) FROM Invoices WHERE PatientID = 'TTRG_P01' AND InvoiceDate = %s", (self.trigger_day_1,))
        self.assertGreaterEqual(cursor.fetchone()[0], 1)

        cursor.execute("SELECT TotalAmount FROM Invoices WHERE PatientID = 'TTRG_P01' AND InvoiceDate = %s LIMIT 1", (self.trigger_day_1,))
        self.assertEqual(float(cursor.fetchone()[0]), 50000.00)
        print("  ✅ Trigger correctly auto-created invoice with 50,000 VND")
        cursor.close()

    def test_trigger_updates_invoice_on_second_appointment(self):
        """
        TODO: Insert 2 appointments same patient same day → invoice amount should increase
        """
        cursor = self.db.get_cursor(dictionary=False)
        cursor.execute("INSERT INTO Appointments VALUES ('TTRG_A02', 'TTRG_D01', 'TTRG_P01', %s, '09:00:00')", (self.trigger_day_2,))
        self.db.commit()
        cursor.execute("SELECT TotalAmount FROM Invoices WHERE PatientID = 'TTRG_P01' AND InvoiceDate = %s LIMIT 1", (self.trigger_day_2,))
        first_amount = float(cursor.fetchone()[0])

        cursor.execute("INSERT IGNORE INTO Doctors VALUES ('TTRG_D02', 'Dr. Trigger Test 2', 'TTRGDPT', 'Testing')")
        self.db.commit()
        cursor.execute("INSERT INTO Appointments VALUES ('TTRG_A03', 'TTRG_D02', 'TTRG_P01', %s, '14:00:00')", (self.trigger_day_2,))
        self.db.commit()

        cursor.execute("SELECT TotalAmount FROM Invoices WHERE PatientID = 'TTRG_P01' AND InvoiceDate = %s LIMIT 1", (self.trigger_day_2,))
        updated_amount = float(cursor.fetchone()[0])
        self.assertGreater(updated_amount, first_amount)
        print(f"  ✅ Invoice updated: {first_amount:,.0f} → {updated_amount:,.0f} VND")
        cursor.close()

    def test_trigger_rejects_negative_invoice(self):
        """
        TODO: Try inserting invoice with negative amount → should raise error
        HINT: Use self.assertRaises(Exception)
        """
        cursor = self.db.get_cursor(dictionary=False)
        with self.assertRaises(Exception):
            cursor.execute("INSERT INTO Invoices (InvoiceID, PatientID, InvoiceDate, TotalAmount) VALUES ('TTRG_INV', 'TTRG_P01', %s, -100.00)", (self.trigger_day_1,))
            self.db.commit()
        self.db.connection.rollback()
        print("  ✅ Negative invoice amount correctly rejected by trigger")
        cursor.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
