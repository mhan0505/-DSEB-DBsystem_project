"""
TEST STORED PROCEDURES - Appointment & Invoice
"""
import sys, os, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database_connection import DatabaseConnection

class TestStoredProcedures(unittest.TestCase):

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
        c.execute("DELETE FROM Appointments WHERE AppointmentID LIKE 'TSP%'")
        c.execute("DELETE FROM Invoices WHERE PatientID LIKE 'TSP%' OR InvoiceID LIKE 'TSP%'")
        c.execute("DELETE FROM Patients WHERE PatientID LIKE 'TSP%'")
        c.execute("DELETE FROM Doctors WHERE DoctorID LIKE 'TSP%'")
        c.execute("DELETE FROM Departments WHERE DepartmentID = 'TSPDPT'")
        c.execute("SET FOREIGN_KEY_CHECKS = 1")
        self.db.commit(); c.close()

    def _setup(self):
        """TODO: Create test department, doctor, and patients."""
        c = self.db.get_cursor(dictionary=False)
        # TODO: Insert test data
        self.db.commit(); c.close()

    def test_sp_schedule_success(self):
        """
        TODO: Call sp_schedule_appointment with valid data
        HINT: c.callproc('sp_schedule_appointment', [id, did, pid, date, time, '', ''])
              result[5] should be 'SUCCESS'
        """
        # TODO: Implement
        pass

    def test_sp_schedule_double_booking(self):
        """
        TODO: Schedule twice at same time → second should return 'ERROR'
        """
        # TODO: Implement
        pass

    def test_sp_generate_invoice(self):
        """
        TODO: Call sp_generate_invoice with valid data
        HINT: result[4] should be 'SUCCESS'
        """
        # TODO: Implement
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
