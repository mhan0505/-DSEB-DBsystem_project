# 🏥 Hospital Management System

> **Course:** Database Management System - NEU DATCOM Lab  
> **Project:** 02 - Hospital Management  
> **Tech Stack:** MySQL + Python


![[Pasted image 20260413113427.png]]
---

## ⭐ Điểm nổi bật

- **Chống Double Booking** - UNIQUE INDEX + Stored Procedure + Python validation (3 lớp bảo vệ)
- **Auto Invoice** - Trigger tự động tạo hóa đơn khi có appointment mới
- **5 Views** - Reports: Daily appointments, Monthly revenue, Doctor stats, Patient history, Department summary
- **5 Stored Procedures** - Tự động hóa: Schedule, Invoice, Cancel, History, Daily report
- **4 UDFs** - Tính toán: Invoice total, Patient age, Doctor workload, Patient spending
- **4 Triggers** - Tự động: Auto invoice, Validate data, Adjust on delete, Block negative
- **5 User Roles** - Security: Admin, Doctor, Receptionist, Accountant, Read-only

---

## 📁 Cấu trúc dự án

```
hospital_management_system/
├── database/
│   ├── scripts/
│   │   ├── 01_DDL_Create_DB.sql
│   │   ├── 02_DDL_Create_Tables.sql          ← UNIQUE INDEX chống double booking
│   │   ├── 03_DML_Insert_Data.sql
│   │   ├── 04_Advanced_Indexes.sql
│   │   ├── 05_Advanced_Views.sql             ← 5 Views cho reports
│   │   ├── 06_Advanced_Procedures.sql        ← 5 Stored Procedures
│   │   ├── 07_Advanced_Functions.sql         ← 4 UDFs
│   │   ├── 08_Advanced_Triggers.sql          ← 4 Triggers
│   │   └── 09_Security_Users.sql             ← 5 User Roles
│   ├── diagrams/
│   └── README_DB.md
├── src/
│   ├── config.py
│   ├── database_connection.py
│   ├── models/          (Patient, Doctor, Department, Appointment, Invoice)
│   ├── repositories/    (CRUD cho 5 bảng)
│   ├── services/        (Business logic: double booking, invoice calc)
│   └── cli/             (Main menu + Reports)
├── tests/
│   ├── test_double_booking.py    ← Test quan trọng nhất
│   ├── test_triggers.py
│   ├── test_stored_procedures.py
│   └── test_crud_real.py
├── docs/
│   ├── BUSINESS_RULES.md
│   ├── DEMO_SCRIPT.md
│   └── REPORT_OUTLINE.md
└── README.md
```

---

## 🚀 Hướng dẫn cài đặt

### 1. Yêu cầu
- MySQL 8.0+
- Python 3.8+
- mysql-connector-python

### 2. Cài đặt dependencies
```bash
pip install mysql-connector-python
```

### 3. Setup database (chạy theo thứ tự)
```bash
mysql -u root -p < database/scripts/01_DDL_Create_DB.sql
mysql -u root -p hospital_db < database/scripts/02_DDL_Create_Tables.sql
mysql -u root -p hospital_db < database/scripts/03_DML_Insert_Data.sql
mysql -u root -p hospital_db < database/scripts/04_Advanced_Indexes.sql
mysql -u root -p hospital_db < database/scripts/05_Advanced_Views.sql
mysql -u root -p hospital_db < database/scripts/06_Advanced_Procedures.sql
mysql -u root -p hospital_db < database/scripts/07_Advanced_Functions.sql
mysql -u root -p hospital_db < database/scripts/08_Advanced_Triggers.sql
mysql -u root -p hospital_db < database/scripts/09_Security_Users.sql
```

### 4. Cấu hình kết nối
Tạo file `.env` từ template:
```bash
cp .env.example .env
```

Sửa file `.env` với thông tin database của bạn:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password_here    # ← Đổi password của bạn
DB_NAME=hospital_db
```

### 5. Chạy ứng dụng

**Giao diện Đồ họa (GUI) - Khuyên dùng:**
Chạy giao diện Desktop hiện đại (có Dark Mode, Dashboard, RBAC Login) để demo:
```bash
python run_gui.py
```

**(Tùy chọn) Chạy giao diện dòng lệnh (CLI):**
```bash
python -m src.cli.main
```

### 6. Chạy tests
```bash
python -m pytest tests/ -v
# hoặc
python -m unittest discover tests/ -v
```

---

## 📊 5 Bảng theo yêu cầu

| Bảng | PK | FK | Đặc biệt |
|------|----|----|-----------|
| Departments | DepartmentID | - | UNIQUE name |
| Patients | PatientID | - | CHECK gender |
| Doctors | DoctorID | → Departments | - |
| Appointments | AppointmentID | → Doctors, Patients | ⭐ UNIQUE INDEX |
| Invoices | InvoiceID | → Patients | DEFAULT 0.00 |

---

## 🔒 Bảo mật hệ thống

### Chống SQL Injection (3 lớp)

| Lớp | Cơ chế | File |
|-----|--------|------|
| 1. Input Validation | Whitelist regex + SQL keyword detection | `src/security/input_validator.py` |
| 2. Parameterized Queries | `%s` placeholders, không nối chuỗi | `src/repositories/*.py` |
| 3. Least Privilege | 5 roles, không có DROP/ALTER | `09_Security_Users.sql` |

### Mã hóa dữ liệu nhạy cảm

- **AES-256** (Fernet) cho `PhoneNumber` và `Address`
- Key quản lý qua `.env` (không commit lên Git)
- File: `src/security/encryption.py`

### 5 User Roles

| Role | Quyền chính |
|------|------------|
| `admin_hospital` | ALL PRIVILEGES |
| `doctor_user` | Đọc bệnh nhân, quản lý lịch hẹn |
| `receptionist` | CRUD bệnh nhân + lịch hẹn |
| `accountant` | Quản lý hóa đơn + báo cáo tài chính |
| `readonly_user` | Chỉ đọc (audit) |

> Chi tiết: `docs/SECURITY_GUIDE.md`

---

## 📐 Chuẩn hóa CSDL

Database đạt **chuẩn 3NF** (Third Normal Form):
- ✅ 1NF: Tất cả giá trị atomic, có Primary Key
- ✅ 2NF: Không phụ thuộc bộ phận (PK đơn)
- ✅ 3NF: Không phụ thuộc bắc cầu (tách đúng qua FK)

> Chi tiết: `docs/NORMALIZATION_3NF.md`

---
