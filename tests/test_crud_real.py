"""
TEST CRUD OPERATIONS - Real database tests
"""
import sys, os, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database_connection import DatabaseConnection
from src.repositories.patient_repository import PatientRepository
from src.repositories.doctor_repository import DoctorRepository
from src.repositories.department_repository import DepartmentRepository
from src.models.patient import Patient
from src.models.department import Department
from datetime import date

class TestCRUD(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = DatabaseConnection()
        cls.db.connect()
        cls.patient_repo = PatientRepository()
        cls.doctor_repo = DoctorRepository()
        cls.dept_repo = DepartmentRepository()

    @classmethod
    def tearDownClass(cls):
        cls.db.disconnect()
        DatabaseConnection._instance = None

    def setUp(self):
        self._cleanup()

    def tearDown(self):
        self._cleanup()

    def _cleanup(self):
        c = self.db.get_cursor(dictionary=False)
        c.execute("SET FOREIGN_KEY_CHECKS = 0")
        c.execute("DELETE FROM Patients WHERE PatientID LIKE 'TCRD%'")
        c.execute("SET FOREIGN_KEY_CHECKS = 1")
        self.db.commit(); c.close()

    def test_create_and_read_patient(self):
        """
        TODO:
        1. Create a Patient object with ID 'TCRD_P01'
        2. Call self.patient_repo.create(patient)
        3. Call self.patient_repo.get_by_id('TCRD_P01')
        4. Assert the returned patient is not None
        5. Assert patient_name matches
        """
        p = Patient('TCRD_P01', 'Test CRUD Patient', date(2000,1,1), 'M', 'HN', '090')
        self.assertTrue(self.patient_repo.create(p))
        found = self.patient_repo.get_by_id('TCRD_P01')
        self.assertIsNotNone(found)
        self.assertEqual(found.patient_name, 'Test CRUD Patient')

    def test_update_patient(self):
        """
        TODO: Create patient, update name, verify change
        """
        p = Patient('TCRD_P02', 'First Name', date(2000,1,1), 'F', 'HN', '091')
        self.patient_repo.create(p)
        p.patient_name = 'Changed Name'
        self.assertTrue(self.patient_repo.update(p))
        found = self.patient_repo.get_by_id('TCRD_P02')
        self.assertEqual(found.patient_name, 'Changed Name')

    def test_delete_patient(self):
        """
        TODO: Create patient, delete it, verify it's gone
        """
        p = Patient('TCRD_P03', 'Remove Test', date(2000,1,1), 'M', 'HN', '092')
        self.patient_repo.create(p)
        self.assertTrue(self.patient_repo.delete('TCRD_P03'))
        self.assertIsNone(self.patient_repo.get_by_id('TCRD_P03'))

    def test_search_by_name(self):
        """
        TODO: Create patient with known name, search by partial name
        """
        p = Patient('TCRD_P04', 'Nguyen Van Search', date(2000,1,1), 'M', 'HN', '093')
        self.patient_repo.create(p)
        results = self.patient_repo.search_by_name('Search')
        self.assertGreater(len(results), 0)

    def test_list_all(self):
        """
        TODO: Call get_all(), verify it returns a list
        """
        patients = self.patient_repo.get_all()
        self.assertIsInstance(patients, list)


if __name__ == '__main__':
    unittest.main(verbosity=2)
