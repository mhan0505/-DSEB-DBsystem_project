"""
Input Validator Module - Chống SQL Injection tầng Application.

PHÒNG CHỐNG SQL INJECTION:
Hệ thống sử dụng 3 lớp bảo vệ:
  1. Parameterized Queries (prepared statements) - Tầng Repository
  2. Input Validation (whitelist) - Tầng này (InputValidator)
  3. Principle of Least Privilege - Tầng Database (phân quyền user)

Tham khảo: SQL_injection.md - Mục 5: Phòng chống SQL Injection
  - Prepared statements / parameterized queries
  - Kiểm tra đầu vào theo whitelist
  - Giới hạn quyền trong cơ sở dữ liệu
  - Xử lý lỗi đúng cách (không hiển thị chi tiết SQL cho user)
"""

import re
from datetime import date, time


class InputValidator:
    """
    Validates and sanitizes all user inputs before they reach the database.
    
    CONCEPT: Whitelist validation
    - Chỉ cho phép các ký tự/format hợp lệ
    - Từ chối tất cả input không đúng mẫu
    - KHÔNG dùng blacklist (dễ bị bypass)
    """

    # =========================================================
    # ID VALIDATION
    # Chỉ cho phép: chữ cái, số, dấu gạch dưới
    # Chặn: dấu nháy đơn, dấu nháy kép, --, ;, UNION, SELECT...
    # =========================================================
    
    # Regex: chỉ cho phép chữ cái, số, gạch dưới
    ID_PATTERN = re.compile(r'^[A-Za-z0-9_]+$')
    
    # Regex: tên người - cho phép Unicode, khoảng trắng, dấu chấm, gạch ngang
    NAME_PATTERN = re.compile(r'^[\w\s\.\-\u00C0-\u024F\u1E00-\u1EFF]+$', re.UNICODE)
    
    # Regex: số điện thoại - chỉ số và dấu +
    PHONE_PATTERN = re.compile(r'^[\d\+\-\s]{0,15}$')
    
    # Regex: địa chỉ - cho phép Unicode, số, khoảng trắng, dấu phẩy, dấu chấm
    ADDRESS_PATTERN = re.compile(r'^[\w\s\,\.\-\/\u00C0-\u024F\u1E00-\u1EFF]*$', re.UNICODE)
    
    # Regex: chuyên khoa
    SPECIALTY_PATTERN = re.compile(r'^[\w\s\&\-\u00C0-\u024F\u1E00-\u1EFF]*$', re.UNICODE)

    # Danh sách các keyword SQL Injection phổ biến (dùng để cảnh báo, KHÔNG phải biện pháp chính)
    SQL_INJECTION_KEYWORDS = [
        "UNION", "SELECT", "INSERT", "UPDATE", "DELETE", "DROP",
        "ALTER", "EXEC", "EXECUTE", "--", ";", "/*", "*/",
        "xp_", "sp_", "SLEEP(", "BENCHMARK(", "OR 1=1",
        "' OR '", "\" OR \"", "1=1", "INFORMATION_SCHEMA"
    ]

    @staticmethod
    def validate_id(value: str, field_name: str = "ID") -> str:
        """
        Validate ID fields (PatientID, DoctorID, etc.)
        
        Chỉ cho phép: chữ cái, số, gạch dưới
        Chặn các ký tự đặc biệt có thể gây SQL Injection:
          - Dấu nháy đơn (')  → dùng để thoát khỏi chuỗi SQL
          - Dấu nháy kép (")  → tương tự
          - Dấu chấm phẩy (;) → kết thúc câu lệnh, chèn lệnh mới
          - Gạch ngang kép (--) → comment SQL, vô hiệu hóa phần còn lại
        
        Args:
            value: Giá trị cần validate
            field_name: Tên trường (để hiển thị lỗi)
            
        Returns:
            Giá trị đã được validate và trim
            
        Raises:
            ValueError: Nếu giá trị không hợp lệ
        """
        if not value or not value.strip():
            raise ValueError(f"{field_name} không được để trống")
        
        value = value.strip()
        
        if len(value) > 10:
            raise ValueError(f"{field_name} không được dài quá 10 ký tự")
        
        if not InputValidator.ID_PATTERN.match(value):
            raise ValueError(
                f"{field_name} chỉ được chứa chữ cái, số và dấu gạch dưới. "
                f"Giá trị '{value}' không hợp lệ."
            )
        
        # Kiểm tra SQL injection keywords (lớp bảo vệ thêm)
        InputValidator._check_sql_keywords(value, field_name)
        
        return value

    @staticmethod
    def validate_name(value: str, field_name: str = "Name") -> str:
        """
        Validate tên người (PatientName, DoctorName, DepartmentName).
        Cho phép Unicode (tên tiếng Việt), khoảng trắng, dấu chấm.
        """
        if not value or not value.strip():
            raise ValueError(f"{field_name} không được để trống")
        
        value = value.strip()
        
        if len(value) > 100:
            raise ValueError(f"{field_name} không được dài quá 100 ký tự")
        
        if not InputValidator.NAME_PATTERN.match(value):
            raise ValueError(
                f"{field_name} chứa ký tự không hợp lệ. "
                f"Chỉ cho phép chữ cái, số, khoảng trắng và dấu chấm."
            )
        
        InputValidator._check_sql_keywords(value, field_name)
        
        return value

    @staticmethod
    def validate_phone(value: str, field_name: str = "Phone") -> str:
        """Validate số điện thoại - chỉ cho phép số, dấu + và dấu -."""
        if not value:
            return None
        
        value = value.strip()
        
        if not InputValidator.PHONE_PATTERN.match(value):
            raise ValueError(
                f"{field_name} chỉ được chứa số, dấu + và dấu -. "
                f"Giá trị '{value}' không hợp lệ."
            )
        
        return value

    @staticmethod
    def validate_address(value: str, field_name: str = "Address") -> str:
        """Validate địa chỉ - cho phép Unicode, số, dấu phẩy."""
        if not value:
            return None
        
        value = value.strip()
        
        if len(value) > 255:
            raise ValueError(f"{field_name} không được dài quá 255 ký tự")
        
        if not InputValidator.ADDRESS_PATTERN.match(value):
            raise ValueError(f"{field_name} chứa ký tự không hợp lệ.")
        
        InputValidator._check_sql_keywords(value, field_name)
        
        return value

    @staticmethod
    def validate_gender(value: str) -> str:
        """Validate giới tính - chỉ cho phép M, F, O (whitelist)."""
        if not value:
            return None
        
        value = value.strip().upper()
        
        if value not in ('M', 'F', 'O'):
            raise ValueError(
                f"Giới tính phải là 'M' (Male), 'F' (Female) hoặc 'O' (Other). "
                f"Giá trị '{value}' không hợp lệ."
            )
        
        return value

    @staticmethod
    def validate_date(value: str, field_name: str = "Date") -> date:
        """
        Validate ngày tháng - chỉ chấp nhận format YYYY-MM-DD.
        
        Chặn injection qua date field:
          Ví dụ attack: "2024-01-01'; DROP TABLE Patients;--"
          → Sẽ bị reject vì không match format date
        """
        if not value or not value.strip():
            raise ValueError(f"{field_name} không được để trống")
        
        value = value.strip()
        
        # Strict format check - chỉ YYYY-MM-DD
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', value):
            raise ValueError(f"{field_name} phải có format YYYY-MM-DD")
        
        try:
            return date.fromisoformat(value)
        except ValueError:
            raise ValueError(f"{field_name} không phải ngày hợp lệ: {value}")

    @staticmethod
    def validate_time(value: str, field_name: str = "Time") -> time:
        """Validate thời gian - chỉ chấp nhận HH:MM hoặc HH:MM:SS."""
        if not value or not value.strip():
            raise ValueError(f"{field_name} không được để trống")
        
        value = value.strip()
        
        # Strict format check
        if not re.match(r'^\d{2}:\d{2}(:\d{2})?$', value):
            raise ValueError(f"{field_name} phải có format HH:MM hoặc HH:MM:SS")
        
        try:
            parts = value.split(':')
            h, m = int(parts[0]), int(parts[1])
            s = int(parts[2]) if len(parts) > 2 else 0
            
            if not (0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59):
                raise ValueError(f"{field_name} không hợp lệ")
            
            return time(h, m, s)
        except (ValueError, IndexError):
            raise ValueError(f"{field_name} không phải thời gian hợp lệ: {value}")

    @staticmethod
    def validate_amount(value, field_name: str = "Amount") -> float:
        """Validate số tiền - phải >= 0."""
        try:
            amount = float(value)
        except (ValueError, TypeError):
            raise ValueError(f"{field_name} phải là số")
        
        if amount < 0:
            raise ValueError(f"{field_name} không được âm")
        
        if amount > 999999999.99:
            raise ValueError(f"{field_name} vượt quá giới hạn cho phép")
        
        return amount

    @staticmethod
    def validate_specialty(value: str, field_name: str = "Specialty") -> str:
        """Validate chuyên khoa."""
        if not value:
            return None
        
        value = value.strip()
        
        if len(value) > 50:
            raise ValueError(f"{field_name} không được dài quá 50 ký tự")
        
        if not InputValidator.SPECIALTY_PATTERN.match(value):
            raise ValueError(f"{field_name} chứa ký tự không hợp lệ.")
        
        InputValidator._check_sql_keywords(value, field_name)
        
        return value

    @staticmethod
    def _check_sql_keywords(value: str, field_name: str):
        """
        Kiểm tra xem input có chứa SQL keyword nguy hiểm không.
        
        LƯU Ý: Đây KHÔNG phải biện pháp chính để chống SQL Injection.
        Biện pháp chính là Parameterized Queries (đã implement ở Repository layer).
        Đây chỉ là lớp bảo vệ bổ sung (defense in depth).
        """
        upper_value = value.upper()
        for keyword in InputValidator.SQL_INJECTION_KEYWORDS:
            if keyword in upper_value:
                raise ValueError(
                    f"{field_name} chứa từ khóa không được phép: '{keyword}'. "
                    f"Vui lòng kiểm tra lại input."
                )

    @staticmethod
    def sanitize_error_message(error: Exception) -> str:
        """
        Xử lý thông báo lỗi - KHÔNG tiết lộ cấu trúc SQL/DB cho user.
        
        Tham khảo SQL_injection.md Mục 5.6:
        "Không hiển thị lỗi SQL chi tiết cho người dùng cuối.
         Thay vào đó, ghi log nội bộ và chỉ thông báo lỗi chung."
        """
        error_str = str(error)
        
        # Danh sách các pattern lỗi SQL cần ẩn
        sensitive_patterns = [
            "mysql", "syntax", "query", "table", "column",
            "database", "SELECT", "INSERT", "UPDATE", "DELETE",
            "FROM", "WHERE", "JOIN", "INDEX"
        ]
        
        for pattern in sensitive_patterns:
            if pattern.lower() in error_str.lower():
                # Log error nội bộ (trong production sẽ ghi vào file log)
                print(f"[SECURITY LOG] SQL Error suppressed: {error_str}")
                return "Đã xảy ra lỗi hệ thống. Vui lòng thử lại sau."
        
        return error_str
