"""
TEST STORED PROCEDURES - Appointment & Invoice
"""
import sys, os, unittest
from datetime import date, timedelta
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
        self.future_date = (date.today() + timedelta(days=7)).isoformat()
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
        c = self.db.get_cursor(dictionary=False)
        c.execute("INSERT IGNORE INTO Departments VALUES ('TSPDPT', 'SP Test')")
        c.execute("INSERT INTO Doctors VALUES ('TSP_D01', 'Dr. SP', 'TSPDPT', 'Test')")
        c.execute("INSERT INTO Patients VALUES ('TSP_P01', 'SP Pat1', '1990-01-01', 'M', 'HN', '090')")
        c.execute("INSERT INTO Patients VALUES ('TSP_P02', 'SP Pat2', '1995-05-05', 'F', 'HCM', '091')")
        self.db.commit(); c.close()

    def test_sp_schedule_success(self):
        """
        TODO: Call sp_schedule_appointment with valid data
        HINT: c.callproc('sp_schedule_appointment', [id, did, pid, date, time, '', ''])
              result[5] should be 'SUCCESS'
        """
        c = self.db.get_cursor(dictionary=False)
        r = c.callproc('sp_schedule_appointment', ['TSP_A01','TSP_D01','TSP_P01',self.future_date,'10:00:00','',''])
        self.db.commit()
        self.assertEqual(r[5], 'SUCCESS')
        c.close()

    def test_sp_schedule_double_booking(self):
        """
        TODO: Schedule twice at same time → second should return 'ERROR'
        """
        c = self.db.get_cursor(dictionary=False)
        c.callproc('sp_schedule_appointment', ['TSP_A02','TSP_D01','TSP_P01',self.future_date,'10:00:00','',''])
        self.db.commit()
        r = c.callproc('sp_schedule_appointment', ['TSP_A03','TSP_D01','TSP_P02',self.future_date,'10:00:00','',''])
        self.db.commit()
        self.assertEqual(r[5], 'ERROR')
        c.close()

    def test_sp_generate_invoice(self):
        """
        TODO: Call sp_generate_invoice with valid data
        HINT: result[4] should be 'SUCCESS'
        """
        c = self.db.get_cursor(dictionary=False)
        r = c.callproc('sp_generate_invoice', ['TSP_INV1','TSP_P01',self.future_date,150000.00,'',''])
        self.db.commit()
        self.assertEqual(r[4], 'SUCCESS')
        c.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
