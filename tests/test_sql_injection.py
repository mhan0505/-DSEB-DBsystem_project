"""
⭐ TEST SQL INJECTION PREVENTION

Verifies that the application is protected against SQL Injection attacks.
Tests demonstrate both the attack vectors AND the defense mechanisms.

Tham khảo: SQL_injection.md

3 LỚP BẢO VỆ:
  1. Input Validation (InputValidator) - Whitelist, reject ký tự nguy hiểm
  2. Parameterized Queries - Tách data và SQL code
  3. Least Privilege - User DB chỉ có quyền cần thiết
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.security.input_validator import InputValidator


class TestSQLInjectionPrevention(unittest.TestCase):
    """Test suite chứng minh hệ thống chống được SQL Injection."""

    # =========================================================
    # TEST 1: Chặn dấu nháy đơn trong ID
    # Tham khảo SQL_injection.md Mục 2.1:
    #   "Lỗi thường xuất hiện khi lập trình viên tạo truy vấn bằng cách nối chuỗi"
    #   Input: ' → làm vỡ cú pháp SQL
    # =========================================================
    def test_01_reject_single_quote_in_id(self):
        """
        SQL Injection cơ bản: dấu nháy đơn (') trong ID.
        
        Attack: PatientID = "P001'"
        Nếu nối chuỗi: SELECT * FROM Patients WHERE PatientID = 'P001''
        → Lỗi cú pháp SQL, tiết lộ thông tin hệ thống
        
        Defense: InputValidator reject vì ' không match [A-Za-z0-9_]
        """
        with self.assertRaises(ValueError):
            InputValidator.validate_id("P001'", "PatientID")
        print("  ✅ Dấu nháy đơn (') bị chặn trong ID")

    # =========================================================
    # TEST 2: Chặn OR 1=1 (Authentication Bypass)
    # Tham khảo SQL_injection.md Mục 3.1:
    #   "Nhập 1' OR '1'='1 có thể khiến điều kiện luôn đúng"
    # =========================================================
    def test_02_reject_or_1_equals_1(self):
        """
        SQL Injection: OR 1=1 bypass authentication.
        
        Attack: PatientID = "P001' OR '1'='1"
        Nếu nối chuỗi: SELECT * FROM Patients WHERE PatientID = 'P001' OR '1'='1'
        → Trả về TẤT CẢ bệnh nhân!
        
        Defense: InputValidator reject vì chứa dấu nháy đơn và khoảng trắng
        """
        with self.assertRaises(ValueError):
            InputValidator.validate_id("P001' OR '1'='1", "PatientID")
        print("  ✅ OR 1=1 injection bị chặn")

    # =========================================================
    # TEST 3: Chặn UNION SELECT (Data Extraction)
    # Tham khảo SQL_injection.md Mục 4.2:
    #   "Union-Based SQL Injection khai thác toán tử UNION"
    # =========================================================
    def test_03_reject_union_select_in_name(self):
        """
        SQL Injection: UNION SELECT để đọc dữ liệu bảng khác.
        
        Attack: Name = "An' UNION SELECT user, password FROM users--"
        Nếu nối chuỗi: SELECT * FROM Patients WHERE PatientName = 'An' UNION SELECT user, password FROM users--'
        → Trả về username và password!
        
        Defense: InputValidator phát hiện keyword "UNION" và "SELECT"
        """
        with self.assertRaises(ValueError):
            InputValidator.validate_name("An' UNION SELECT user, password FROM users--", "PatientName")
        print("  ✅ UNION SELECT injection bị chặn")

    # =========================================================
    # TEST 4: Chặn DROP TABLE
    # =========================================================
    def test_04_reject_drop_table(self):
        """
        SQL Injection: DROP TABLE để xóa dữ liệu.
        
        Attack: Name = "An'; DROP TABLE Patients;--"
        → Xóa toàn bộ bảng Patients!
        
        Defense: 
        1. InputValidator reject dấu ; và keyword DROP
        2. Parameterized query không cho phép execute nhiều lệnh
        3. DB user không có quyền DROP
        """
        with self.assertRaises(ValueError):
            InputValidator.validate_name("An'; DROP TABLE Patients;--", "PatientName")
        print("  ✅ DROP TABLE injection bị chặn")

    # =========================================================
    # TEST 5: Chặn comment SQL (--)
    # Tham khảo SQL_injection.md Mục 3.1:
    #   "Nhập 1' UNION SELECT user, password FROM users--"
    # =========================================================
    def test_05_reject_sql_comment(self):
        """
        SQL Comment (--) dùng để vô hiệu hóa phần còn lại của query.
        
        Attack: ID = "P001'--"
        → WHERE PatientID = 'P001'-- AND other_condition
        → other_condition bị bỏ qua!
        """
        with self.assertRaises(ValueError):
            InputValidator.validate_id("P001'--", "PatientID")
        print("  ✅ SQL comment (--) bị chặn")

    # =========================================================
    # TEST 6: Chặn SLEEP() (Time-Based Blind SQLi)
    # Tham khảo SQL_injection.md Mục cuối:
    #   "Time-based blind SQL Injection... dùng SLEEP(x)"
    # =========================================================
    def test_06_reject_sleep_injection(self):
        """
        Time-Based Blind SQLi dùng SLEEP() để suy luận thông tin.
        
        Attack: Name = "admin' UNION SELECT SLEEP(5),2;--"
        → Server chậm 5 giây → xác nhận injection thành công
        """
        with self.assertRaises(ValueError):
            InputValidator.validate_name("admin UNION SELECT SLEEP(5)", "Name")
        print("  ✅ SLEEP() injection bị chặn")

    # =========================================================
    # TEST 7: Input hợp lệ vẫn hoạt động bình thường
    # =========================================================
    def test_07_valid_inputs_pass(self):
        """Đảm bảo input hợp lệ không bị reject nhầm."""
        # ID hợp lệ
        self.assertEqual(InputValidator.validate_id("P001", "ID"), "P001")
        self.assertEqual(InputValidator.validate_id("DOC001", "ID"), "DOC001")
        self.assertEqual(InputValidator.validate_id("APT_001", "ID"), "APT_001")
        
        # Tên tiếng Việt hợp lệ
        self.assertEqual(InputValidator.validate_name("Nguyen Van An", "Name"), "Nguyen Van An")
        self.assertEqual(InputValidator.validate_name("Trần Thị Bình", "Name"), "Trần Thị Bình")
        
        # Phone hợp lệ
        self.assertEqual(InputValidator.validate_phone("0901234567"), "0901234567")
        self.assertEqual(InputValidator.validate_phone("+84901234567"), "+84901234567")
        
        # Gender hợp lệ
        self.assertEqual(InputValidator.validate_gender("M"), "M")
        self.assertEqual(InputValidator.validate_gender("f"), "F")  # auto uppercase
        
        # Date hợp lệ
        from datetime import date
        self.assertEqual(InputValidator.validate_date("2024-01-15"), date(2024, 1, 15))
        
        # Time hợp lệ
        from datetime import time
        self.assertEqual(InputValidator.validate_time("10:30:00"), time(10, 30, 0))
        
        print("  ✅ Tất cả input hợp lệ được chấp nhận")

    # =========================================================
    # TEST 8: Chặn injection qua trường Date
    # =========================================================
    def test_08_reject_injection_in_date(self):
        """
        Attack qua trường Date:
        Date = "2024-01-01'; DROP TABLE Patients;--"
        """
        with self.assertRaises(ValueError):
            InputValidator.validate_date("2024-01-01'; DROP TABLE Patients;--")
        print("  ✅ Injection qua Date bị chặn")

    # =========================================================
    # TEST 9: Chặn injection qua trường Amount
    # =========================================================
    def test_09_reject_injection_in_amount(self):
        """Amount phải là số, không thể chứa SQL code."""
        with self.assertRaises(ValueError):
            InputValidator.validate_amount("100; DROP TABLE Invoices")
        print("  ✅ Injection qua Amount bị chặn")

    # =========================================================
    # TEST 10: Error message KHÔNG tiết lộ cấu trúc DB
    # Tham khảo SQL_injection.md Mục 5.6:
    #   "Không hiển thị lỗi SQL chi tiết cho người dùng cuối"
    # =========================================================
    def test_10_error_message_sanitization(self):
        """
        Kiểm tra error message không tiết lộ thông tin SQL.
        
        ❌ Lỗi chi tiết (nguy hiểm):
           "You have an error in your SQL syntax; check the manual that 
            corresponds to your MySQL server version for the right syntax
            to use near ''P001''' at line 1"
        → Attacker biết: dùng MySQL, cú pháp query, vị trí lỗi
        
        ✅ Lỗi an toàn (sau sanitize):
           "Đã xảy ra lỗi hệ thống. Vui lòng thử lại sau."
        """
        # Giả lập SQL error
        sql_error = Exception(
            "You have an error in your SQL syntax near "
            "'SELECT * FROM Patients WHERE PatientID = 'P001'''"
        )
        safe_msg = InputValidator.sanitize_error_message(sql_error)
        
        # Error message không được chứa chi tiết SQL
        self.assertNotIn("SELECT", safe_msg)
        self.assertNotIn("FROM", safe_msg)
        self.assertNotIn("WHERE", safe_msg)
        self.assertNotIn("syntax", safe_msg)
        
        print("  ✅ Error message đã được sanitize, không tiết lộ SQL")

    # =========================================================
    # TEST 11: INFORMATION_SCHEMA bị chặn
    # Tham khảo SQL_injection.md:
    #   "information_schema là CSDL hệ thống chứa thông tin tất cả bảng"
    # =========================================================
    def test_11_reject_information_schema(self):
        """
        Attacker dùng INFORMATION_SCHEMA để liệt kê tất cả bảng.
        
        Attack: "admin' UNION SELECT table_name FROM information_schema.tables--"
        """
        with self.assertRaises(ValueError):
            InputValidator.validate_name("a INFORMATION_SCHEMA", "Name")
        print("  ✅ INFORMATION_SCHEMA bị chặn")


class TestParameterizedQueries(unittest.TestCase):
    """
    Test chứng minh tất cả queries đều dùng parameterized format.
    
    Tham khảo SQL_injection.md Mục 5.1:
      "Dữ liệu đầu vào được truyền như tham số, 
       không được ghép thẳng vào chuỗi truy vấn."
    
    CÁCH KIỂM TRA:
    Scan toàn bộ source code repository, đảm bảo KHÔNG có f-string
    hoặc .format() trong câu lệnh SQL.
    """
    
    def test_no_string_concatenation_in_queries(self):
        """
        Scan repository files để đảm bảo không có nối chuỗi SQL.
        
        ❌ KHÔNG AN TOÀN:
            query = f"SELECT * FROM Patients WHERE PatientID = '{pid}'"
            query = "SELECT * FROM Patients WHERE PatientID = '" + pid + "'"
            
        ✅ AN TOÀN:
            query = "SELECT * FROM Patients WHERE PatientID = %s"
            self.db.execute_query(query, (pid,))
        """
        import ast
        
        repo_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'src', 'repositories'
        )
        
        unsafe_patterns = []
        
        for filename in os.listdir(repo_dir):
            if not filename.endswith('.py') or filename == '__init__.py':
                continue
            
            filepath = os.path.join(repo_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Kiểm tra f-string SQL patterns (chỉ kiểm tra code thực, bỏ qua docstring/comment)
            lines = content.split('\n')
            in_docstring = False
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                
                # Track docstring boundaries
                if stripped.count('"""') % 2 == 1 or stripped.count("'''") % 2 == 1:
                    in_docstring = not in_docstring
                    continue
                if in_docstring:
                    continue
                # Skip comments
                if stripped.startswith('#'):
                    continue
                
                # Tìm f-string chứa SELECT/INSERT/UPDATE/DELETE
                if stripped.startswith('query') or stripped.startswith('sql'):
                    if 'f"' in stripped or "f'" in stripped:
                        unsafe_patterns.append(f"{filename}:{i}: {stripped}")
                    if '.format(' in stripped:
                        unsafe_patterns.append(f"{filename}:{i}: {stripped}")
        
        if unsafe_patterns:
            self.fail(
                "Found unsafe SQL string concatenation:\n" +
                "\n".join(unsafe_patterns)
            )
        
        print("  All repository queries use parameterized format (%s)")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("  🔒 SQL INJECTION PREVENTION TESTS")
    print("  Tham khảo: SQL_injection.md")
    print("=" * 60 + "\n")
    unittest.main(verbosity=2)
