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
from datetime import date

class TestCRUD(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = DatabaseConnection()
        cls.db.connect()
        cls.patient_repo = PatientRepository()

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
        # TODO: Implement
        pass

    def test_update_patient(self):
        """
        TODO: Create patient, update name, verify change
        """
        # TODO: Implement
        pass

    def test_delete_patient(self):
        """
        TODO: Create patient, delete it, verify it's gone
        """
        # TODO: Implement
        pass

    def test_search_by_name(self):
        """
        TODO: Create patient with known name, search by partial name
        """
        # TODO: Implement
        pass

    def test_list_all(self):
        """
        TODO: Call get_all(), verify it returns a list
        """
        # TODO: Implement
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
