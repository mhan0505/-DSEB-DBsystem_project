# 🏥 Hospital Management System

> **Course:** Database Management System - NEU DATCOM Lab  
> **Project:** 02 - Hospital Management  
> **Tech Stack:** MySQL + Python

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
```bash
cd hospital_management_system
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

