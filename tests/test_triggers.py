"""
⭐ TEST TRIGGERS - Auto Invoice Generation

Verifies: trg_after_appointment_insert trigger auto-creates invoices.
"""

import sys, os, unittest
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
        """TODO: Create test department, doctor, and patient."""
        c = self.db.get_cursor(dictionary=False)
        # TODO: Insert test data
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
        # TODO: Implement
        pass

    def test_trigger_updates_invoice_on_second_appointment(self):
        """
        TODO: Insert 2 appointments same patient same day → invoice amount should increase
        """
        # TODO: Implement
        pass

    def test_trigger_rejects_negative_invoice(self):
        """
        TODO: Try inserting invoice with negative amount → should raise error
        HINT: Use self.assertRaises(Exception)
        """
        # TODO: Implement
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
