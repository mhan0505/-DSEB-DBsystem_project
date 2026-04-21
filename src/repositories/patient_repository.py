"""
Patient Repository - CRUD operations for Patients table.

CONCEPT: Repository Pattern
- This class handles ALL database operations for Patients
- Other code should NEVER write SQL for Patients directly
- Always use this repository instead

SECURITY:
- Tất cả queries đều dùng Parameterized Queries (%s) → chống SQL Injection
- Dữ liệu nhạy cảm (PhoneNumber, Address) được mã hóa AES trước khi lưu
- Input được validate qua InputValidator trước khi execute
"""

from src.database_connection import DatabaseConnection
from src.models.patient import Patient
from src.security.encryption import get_encryption
from src.security.input_validator import InputValidator


class PatientRepository:
    """Data access layer for Patient entity."""

    def __init__(self):
        self.db = DatabaseConnection()
        self.encryption = get_encryption()

    def _encrypt_patient_data(self, patient: Patient) -> tuple:
        """
        Mã hóa dữ liệu nhạy cảm của bệnh nhân trước khi lưu vào DB.
        
        Trường được mã hóa:
          - PhoneNumber: số điện thoại cá nhân
          - Address: địa chỉ nhà
        
        Trường KHÔNG mã hóa (cần dùng cho truy vấn/JOIN):
          - PatientID, PatientName, DateOfBirth, Gender
        """
        encrypted_phone = self.encryption.encrypt(patient.phone_number)
        encrypted_address = self.encryption.encrypt(patient.address)
        return encrypted_phone, encrypted_address

    def _decrypt_patient_data(self, row: dict) -> dict:
        """
        Giải mã dữ liệu nhạy cảm sau khi đọc từ DB.
        """
        if row.get('PhoneNumber'):
            row['PhoneNumber'] = self.encryption.decrypt(row['PhoneNumber'])
        if row.get('Address'):
            row['Address'] = self.encryption.decrypt(row['Address'])
        return row

    def get_all(self) -> list:
        """
        Get all patients from database.

        SECURITY: Dùng parameterized query (không có user input trực tiếp)
        Dữ liệu nhạy cảm được giải mã sau khi đọc.
        """
        query = "SELECT * FROM Patients ORDER BY PatientID"
        results = self.db.execute_query(query)
        # Giải mã dữ liệu nhạy cảm
        decrypted_results = [self._decrypt_patient_data(row) for row in results]
        return [Patient.from_dict(row) for row in decrypted_results]

    def get_by_id(self, patient_id: str) -> Patient:
        """
        Get a single patient by their ID.

        SECURITY:
        - patient_id được validate trước khi execute
        - Query dùng parameterized query (%s) → chống SQL Injection
        
        VÍ DỤ CHỐNG SQL INJECTION:
        ❌ KHÔNG AN TOÀN (nối chuỗi):
            query = f"SELECT * FROM Patients WHERE PatientID = '{patient_id}'"
            → Nếu patient_id = "P001' OR '1'='1" → trả về TẤT CẢ bệnh nhân!
            
        ✅ AN TOÀN (parameterized query - cách chúng ta dùng):
            query = "SELECT * FROM Patients WHERE PatientID = %s"
            params = (patient_id,)
            → Dù input là gì, MySQL xử lý nó như DATA, không phải SQL code
        """
        # Bước 1: Validate input
        patient_id = InputValidator.validate_id(patient_id, "PatientID")
        
        # Bước 2: Execute với parameterized query
        query = "SELECT * FROM Patients WHERE PatientID = %s"
        results = self.db.execute_query(query, (patient_id,))
        if results:
            decrypted = self._decrypt_patient_data(results[0])
            return Patient.from_dict(decrypted)
        return None

    def search_by_name(self, name: str) -> list:
        """
        Search patients by name (partial match).

        SECURITY:
        - name được validate trước
        - Dùng parameterized query với LIKE
        - Input name được đặt trong %...% nhưng VẪN là parameter, KHÔNG nối chuỗi
        """
        # Validate input
        name = InputValidator.validate_name(name, "Search Name")
        
        query = "SELECT * FROM Patients WHERE PatientName LIKE %s ORDER BY PatientName"
        results = self.db.execute_query(query, (f"%{name}%",))
        decrypted_results = [self._decrypt_patient_data(row) for row in results]
        return [Patient.from_dict(row) for row in decrypted_results]

    def create(self, patient: Patient) -> bool:
        """
        Insert a new patient into database.

        SECURITY:
        - Input validation cho tất cả fields
        - PhoneNumber, Address được mã hóa trước khi lưu
        - Parameterized query cho INSERT
        """
        # Bước 1: Validate tất cả input
        InputValidator.validate_id(patient.patient_id, "PatientID")
        InputValidator.validate_name(patient.patient_name, "PatientName")
        if patient.gender:
            InputValidator.validate_gender(patient.gender)
        if patient.phone_number:
            InputValidator.validate_phone(patient.phone_number, "PhoneNumber")
        if patient.address:
            InputValidator.validate_address(patient.address, "Address")
        
        # Bước 2: Mã hóa dữ liệu nhạy cảm
        encrypted_phone, encrypted_address = self._encrypt_patient_data(patient)
        
        # Bước 3: Execute với parameterized query
        query = """
            INSERT INTO Patients (PatientID, PatientName, DateOfBirth, Gender, Address, PhoneNumber)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            patient.patient_id, patient.patient_name,
            patient.date_of_birth, patient.gender,
            encrypted_address, encrypted_phone
        )
        affected = self.db.execute_query(query, params, fetch=False)
        return affected > 0

    def update(self, patient: Patient) -> bool:
        """
        Update an existing patient.

        SECURITY: Validate + Encrypt + Parameterized query
        """
        # Validate
        InputValidator.validate_id(patient.patient_id, "PatientID")
        InputValidator.validate_name(patient.patient_name, "PatientName")
        
        # Mã hóa
        encrypted_phone, encrypted_address = self._encrypt_patient_data(patient)
        
        query = """
            UPDATE Patients
            SET PatientName = %s, DateOfBirth = %s, Gender = %s,
                Address = %s, PhoneNumber = %s
            WHERE PatientID = %s
        """
        params = (
            patient.patient_name, patient.date_of_birth,
            patient.gender, encrypted_address,
            encrypted_phone, patient.patient_id
        )
        affected = self.db.execute_query(query, params, fetch=False)
        return affected > 0

    def delete(self, patient_id: str) -> bool:
        """
        Delete a patient by ID.

        SECURITY: Validate ID trước khi DELETE
        NOTE: May fail if patient has appointments/invoices (FK constraint)
        """
        patient_id = InputValidator.validate_id(patient_id, "PatientID")
        query = "DELETE FROM Patients WHERE PatientID = %s"
        affected = self.db.execute_query(query, (patient_id,), fetch=False)
        return affected > 0

    def count(self) -> int:
        """Count total patients."""
        query = "SELECT COUNT(*) AS total FROM Patients"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
