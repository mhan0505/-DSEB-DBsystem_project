# 🔒 BẢO MẬT HỆ THỐNG - HOSPITAL MANAGEMENT SYSTEM

> **Tài liệu tổng hợp các biện pháp bảo mật đã implement trong hệ thống**  
> **Tham khảo:** `SQL_injection.md`

---

## 1. TỔNG QUAN BẢO MẬT

Hệ thống áp dụng mô hình **Defense in Depth** (phòng thủ nhiều lớp):

```
                    ┌─────────────────────────┐
                    │    USER INPUT           │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
          Lớp 1 →  │  INPUT VALIDATION       │  src/security/input_validator.py
                    │  (Whitelist + Regex)     │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
          Lớp 2 →  │  DATA ENCRYPTION        │  src/security/encryption.py
                    │  (AES-256 Fernet)       │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
          Lớp 3 →  │  PARAMETERIZED QUERIES  │  src/repositories/*.py
                    │  (Prepared Statements)  │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
          Lớp 4 →  │  DATABASE PRIVILEGES    │  09_Security_Users.sql
                    │  (Least Privilege)      │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
          Lớp 5 →  │  ERROR HANDLING         │  sanitize_error_message()
                    │  (Ẩn chi tiết SQL)      │
                    └─────────────────────────┘
```

---

## 2. CHỐNG SQL INJECTION (Chi tiết)

### 2.1. Parameterized Queries (Biện pháp chính)

**Tham khảo:** `SQL_injection.md` Mục 5.1

Toàn bộ repository sử dụng **parameterized queries** thay vì nối chuỗi:

```python
# ❌ KHÔNG AN TOÀN (nối chuỗi) - Hệ thống KHÔNG dùng cách này
query = f"SELECT * FROM Patients WHERE PatientID = '{user_input}'"
# Attack: user_input = "P001' OR '1'='1"
# → SELECT * FROM Patients WHERE PatientID = 'P001' OR '1'='1'
# → Trả về TẤT CẢ bệnh nhân!

# ✅ AN TOÀN (parameterized query) - Cách hệ thống dùng
query = "SELECT * FROM Patients WHERE PatientID = %s"
results = self.db.execute_query(query, (user_input,))
# Attack: user_input = "P001' OR '1'='1"
# → MySQL xử lý toàn bộ string "P001' OR '1'='1" như DATA
# → Trả về 0 kết quả (không tìm thấy PatientID này)
```

**Files áp dụng:**
- `src/repositories/patient_repository.py` - Tất cả CRUD
- `src/repositories/doctor_repository.py` - Tất cả CRUD
- `src/repositories/department_repository.py` - Tất cả CRUD
- `src/repositories/appointment_repository.py` - Tất cả CRUD + double booking check
- `src/repositories/invoice_repository.py` - Tất cả CRUD

### 2.2. Input Validation (Whitelist)

**Tham khảo:** `SQL_injection.md` Mục 5.3

File: `src/security/input_validator.py`

| Method | Regex/Rule | Chặn được |
|--------|-----------|-----------|
| `validate_id()` | `^[A-Za-z0-9_]+$` | `'`, `"`, `;`, `--`, spaces |
| `validate_name()` | `^[\w\s\.\-\u00C0-\u1EFF]+$` | `'`, `"`, `;`, `--`, `()` |
| `validate_phone()` | `^[\d\+\-\s]{0,15}$` | Tất cả ký tự không phải số |
| `validate_date()` | `^\d{4}-\d{2}-\d{2}$` | SQL commands, special chars |
| `validate_time()` | `^\d{2}:\d{2}(:\d{2})?$` | SQL commands, special chars |
| `validate_amount()` | `float()` conversion | Non-numeric input |
| `validate_gender()` | Whitelist: M, F, O | Tất cả giá trị khác |

**SQL keyword detection** (lớp bổ sung):
```python
SQL_INJECTION_KEYWORDS = [
    "UNION", "SELECT", "INSERT", "UPDATE", "DELETE", "DROP",
    "ALTER", "--", ";", "/*", "*/", "SLEEP(", "INFORMATION_SCHEMA"
]
```

### 2.3. Stored Procedures

**Tham khảo:** `SQL_injection.md` Mục 5.2

Stored procedures giảm việc tạo query động:
- `sp_schedule_appointment` - Đặt lịch có validation
- `sp_generate_invoice` - Tạo hóa đơn có validation
- `sp_cancel_appointment` - Hủy lịch có validation

### 2.4. Error Handling An Toàn

**Tham khảo:** `SQL_injection.md` Mục 5.6

```python
# ❌ Lỗi chi tiết (nguy hiểm - tiết lộ cấu trúc DB)
"You have an error in your SQL syntax near 'SELECT * FROM Patients WHERE...'"

# ✅ Lỗi đã sanitize (an toàn)
"Đã xảy ra lỗi hệ thống. Vui lòng thử lại sau."
```

File: `InputValidator.sanitize_error_message()` tự động ẩn SQL details.

### 2.5. Test Coverage

File: `tests/test_sql_injection.py` - **12 test cases:**

| Test | Attack Vector | Kết quả |
|------|-------------|---------|
| `test_01` | Dấu nháy đơn (`'`) | ✅ Bị chặn |
| `test_02` | `OR 1=1` bypass | ✅ Bị chặn |
| `test_03` | `UNION SELECT` | ✅ Bị chặn |
| `test_04` | `DROP TABLE` | ✅ Bị chặn |
| `test_05` | SQL comment (`--`) | ✅ Bị chặn |
| `test_06` | `SLEEP()` blind SQLi | ✅ Bị chặn |
| `test_07` | Input hợp lệ | ✅ Được chấp nhận |
| `test_08` | Injection qua Date | ✅ Bị chặn |
| `test_09` | Injection qua Amount | ✅ Bị chặn |
| `test_10` | Error sanitization | ✅ SQL ẩn đi |
| `test_11` | `INFORMATION_SCHEMA` | ✅ Bị chặn |
| `test_12` | No string concat | ✅ Tất cả repos an toàn |

---

## 3. MÃ HÓA DỮ LIỆU NHẠY CẢM

### 3.1. Dữ liệu được mã hóa

| Trường | Bảng | Lý do |
|--------|------|-------|
| **PhoneNumber** | Patients | Thông tin liên lạc cá nhân (PII) |
| **Address** | Patients | Địa chỉ nhà (PII) |

### 3.2. Thuật toán mã hóa

- **Fernet** (from `cryptography` library)
- Bên trong: **AES-128-CBC** + **HMAC-SHA256**
- Key: đọc từ `ENCRYPTION_KEY` trong `.env`
- Mỗi lần encrypt tạo ciphertext khác nhau (random IV) → chống replay attack

### 3.3. Flow mã hóa

```
WRITE: User Input → Validate → Encrypt → Store ciphertext in DB
READ:  DB ciphertext → Decrypt → Display to User

Ví dụ:
  Input: "0901234567"
  Encrypt: "gAAAAABl7x4hK3nR8..."  (lưu trong DB)
  Decrypt: "0901234567"             (hiển thị cho user)
```

### 3.4. Key Management

```env
# File .env (KHÔNG commit lên Git - đã thêm vào .gitignore)
ENCRYPTION_KEY=your-secret-key-here

# Key phải:
# - Dài ít nhất 16 ký tự
# - Khác nhau giữa dev và production
# - Được backup an toàn
# - Thay đổi định kỳ
```

### 3.5. File Implementation

| File | Vai trò |
|------|---------|
| `src/security/encryption.py` | Module mã hóa/giải mã (Fernet AES) |
| `src/repositories/patient_repository.py` | Encrypt khi CREATE/UPDATE, decrypt khi READ |
| `tests/test_encryption.py` | 6 test cases cho encryption |

---

## 4. PHÂN QUYỀN NGƯỜI DÙNG

### 4.1. Nguyên tắc Least Privilege

**Tham khảo:** `SQL_injection.md` Mục 5.5

> "Tài khoản mà ứng dụng dùng để kết nối cơ sở dữ liệu chỉ nên có đúng các quyền cần thiết."

### 4.2. Ma trận phân quyền

| Role | Username | Password (Mặc định) | Patients | Doctors | Departments | Appointments | Invoices | Views | Procedures |
|------|---------|--------------------|---------|---------|------------|-------------|---------|-------|-----------|
| **admin_hospital** | `admin_hospital` | `Admin@Hospital2024!` | ALL | ALL | ALL | ALL | ALL | ALL | ALL |
| **doctor_user** | `doctor_user` | `Doctor@Hospital2024!` | SELECT | SELECT | SELECT | S/I/U | SELECT | 3 views | 2 procs |
| **receptionist** | `receptionist` | `Reception@Hospital2024!` | S/I/U | SELECT | SELECT | S/I/U/D | SELECT | 2 views | 3 procs |
| **accountant** | `accountant` | `Account@Hospital2024!` | SELECT | - | - | SELECT | S/I/U | 3 views | 2 procs |
| **readonly_user** | `readonly_user` | `ReadOnly@Hospital2024!` | SELECT | SELECT | SELECT | SELECT | SELECT | ALL | - |

> ⚠️ **Lưu ý:** Các mật khẩu trên chỉ dùng cho môi trường Demo/Development (được định nghĩa trong `scripts/09_Security_Users.sql`). Trong thực tế (Production), mật khẩu phải được thay đổi và quản lý bảo mật.

*S=SELECT, I=INSERT, U=UPDATE, D=DELETE*

### 4.3. Quyền bị hạn chế

Không role nào (trừ admin) có quyền:
- `DROP TABLE` → Không thể xóa bảng
- `ALTER TABLE` → Không thể thay đổi cấu trúc
- `CREATE/DROP USER` → Không thể tạo/xóa user
- `GRANT` → Không thể cấp quyền cho người khác

---

## 5. CHUẨN HÓA CƠ SỞ DỮ LIỆU

Xem chi tiết tại: `docs/NORMALIZATION_3NF.md`

**Kết luận:** Database đạt chuẩn **3NF** (Third Normal Form)
- ✅ 1NF: Tất cả giá trị atomic, có PK
- ✅ 2NF: Không phụ thuộc bộ phận (tất cả PK đơn)
- ✅ 3NF: Không phụ thuộc bắc cầu (dữ liệu tách đúng qua FK)

---

## 6. CÁC BIỆN PHÁP BỔ SUNG

### 6.1. Transaction Management
```python
# Sử dụng autocommit=False → mỗi operation phải commit rõ ràng
# Nếu có lỗi → rollback toàn bộ
try:
    cursor.execute(query, params)
    self.commit()
except Error:
    self.rollback()
    raise
```

### 6.2. Connection Security
```python
# .env lưu riêng credentials, KHÔNG hardcode trong source
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    ...
}
```

### 6.3. Backup & Recovery
```bash
# Full backup (bao gồm routines và triggers)
mysqldump -u admin_hospital -p --routines --triggers hospital_db > backup.sql

# Restore
mysql -u admin_hospital -p hospital_db < backup.sql
```

---

## 7. CHECKLIST BẢO MẬT

- [x] Parameterized queries cho tất cả SQL operations
- [x] Input validation (whitelist regex) cho tất cả user input
- [x] SQL keyword detection (lớp bảo vệ bổ sung)
- [x] Mã hóa AES cho dữ liệu nhạy cảm (PhoneNumber, Address)
- [x] Encryption key quản lý qua .env (không commit)
- [x] 5 roles phân quyền theo Least Privilege
- [x] Error message sanitization (ẩn SQL details)
- [x] Transaction management (rollback on error)
- [x] Database đạt chuẩn 3NF
- [x] Test coverage cho SQL Injection (12 test cases)
- [x] Test coverage cho Encryption (6 test cases)
- [x] .env trong .gitignore
