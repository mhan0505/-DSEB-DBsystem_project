# 🚀 KẾ HOẠCH 20 NGÀY - HOSPITAL MANAGEMENT SYSTEM
## (TỐI ƯU ĐIỂM SỐ - EFFORT THẤP NHẤT)

---

## 📅 TIMELINE CHI TIẾT (20 NGÀY)

### **WEEK 1: DATABASE FOUNDATION (Ngày 1-7)**

| Ngày | Công việc | Người phụ trách | Deliverable |
|------|-----------|-----------------|-------------|
| **1** | Setup môi trường (MySQL, VS Code, Git), phân công task | All | Repo GitHub, .env, requirements.txt |
| **2** | Thiết kế ERD trên MySQL Workbench | Member 1 | ERD.png |
| **3** | Viết 01_DDL_Create_DB.sql + 02_DDL_Create_Tables.sql | Member 1 | 2 SQL scripts |
| **4** | Viết 03_DML_Insert_Data.sql (5-10 records/bảng) | Member 1 | Sample data |
| **5** | Viết 04_Indexes.sql + 05_Views.sql | Member 2 | Indexes + Views |
| **6** | Viết 06_Procedures.sql + 07_Functions.sql | Member 2 | Procs + Funcs |
| **7** | Viết 08_Triggers.sql + 09_Security.sql | Member 2 | Triggers + Security |

**✅ End Week 1:** Database hoàn chỉnh, chạy được trên Workbench

---

### **WEEK 2-3: PYTHON APPLICATION (Ngày 8-14)**

| Ngày | Công việc | Người phụ trách | Deliverable |
|------|-----------|-----------------|-------------|
| **8** | database_connection.py + config.py | Member 3 | DB connection working |
| **9** | models/ (5 files: Patient, Doctor, Dept, Appt, Invoice) | Member 3 | Model classes |
| **10** | repositories/ (CRUD cho 5 bảng) | Member 3 | Repository layer |
| **11** | services/ (business logic + validation) | Member 3 + 4 | Service layer |
| **12** | cli/main.py + patient_menu.py + doctor_menu.py | Member 4 | CLI menus |
| **13** | cli/appointment_menu.py + report_menu.py | Member 4 | CLI complete |
| **14** | Test toàn bộ Python app + fix bugs | Member 3 + 4 | Working CLI app |

**✅ End Week 3:** Python CLI hoàn chỉnh, CRUD được hết

---

### **WEEK 4: TESTING + REPORT (Ngày 15-20)**

| Ngày | Công việc | Người phụ trách | Deliverable |
|------|-----------|-----------------|-------------|
| **15** | Viết tests (test_crud.py + test_double_booking.py) | Member 5 | Test files |
| **16** | Setup GitHub Actions CI (optional) | Member 5 | CI pipeline |
| **17** | Viết Report: Chương 1-3 (Intro + Analysis + Design) | Member 1 + 5 | 10 pages |
| **18** | Viết Report: Chương 4-6 (Implementation + Testing + Results) | Member 2 + 5 | 10 pages |
| **19** | Viết Report: Chương 7-8 (Conclusion + References) + Review | All | 20-30 pages complete |
| **20** | Final demo rehearsal + submit | All | **SUBMIT** |

**✅ End Week 4:** Báo cáo 20-30 trang + Demo ready

---

## 👥 PHÂN CÔNG CHI TIẾT (4-5 THÀNH VIÊN)

| Member | Vai trò | Nhiệm vụ cụ thể | Deadline |
|--------|---------|-----------------|----------|
| **Member 1** | DB Lead | ERD, 01-03 SQL, Report Ch1-3 | Ngày 7 + 17 |
| **Member 2** | DB Dev | 04-09 SQL (Advanced Objects), Report Ch4 | Ngày 7 + 18 |
| **Member 3** | Python Lead | connection.py, models/, repositories/, services/ | Ngày 11 |
| **Member 4** | CLI Dev | cli/ menus, Report Ch5 | Ngày 14 + 18 |
| **Member 5** | QA & Docs | Tests, CI, Report Ch6-8, Final review | Ngày 19 |

---

## 📁 CẤU TRÚC PROJECT (COPY NGAY)

```
hospital_management_system/
│
├──  database/
│   ├──  scripts/
│   │   ├── 01_DDL_Create_DB.sql
│   │   ├── 02_DDL_Create_Tables.sql
│   │   ├── 03_DML_Insert_Data.sql
│   │   ├── 04_Advanced_Indexes.sql
│   │   ├── 05_Advanced_Views.sql
│   │   ├── 06_Advanced_Procedures.sql
│   │   ├── 07_Advanced_Functions.sql
│   │   ├── 08_Advanced_Triggers.sql
│   │   └── 09_Security_Users.sql
│   ├── 📁 diagrams/
│   │   └── ERD_Workbench.png
│   └── README_DB.md
│
├──  src/
│   ├── __init__.py
│   ├── config.py
│   ├── database_connection.py
│   ├── 📁 models/
│   │   ├── __init__.py
│   │   ├── patient.py
│   │   ├── doctor.py
│   │   ├── department.py
│   │   ├── appointment.py
│   │   └── invoice.py
│   ├── 📁 repositories/
│   │   ├── __init__.py
│   │   ├── patient_repo.py
│   │   ├── doctor_repo.py
│   │   ├── department_repo.py
│   │   ├── appointment_repo.py
│   │   └── invoice_repo.py
│   ├── 📁 services/
│   │   ├── __init__.py
│   │   ├── patient_service.py
│   │   ├── doctor_service.py
│   │   ├── appointment_service.py
│   │   ├── invoice_service.py
│   │   └── report_service.py
│   └── 📁 cli/
│       ├── __init__.py
│       ├── main.py
│       ├── patient_menu.py
│       ├── doctor_menu.py
│       ├── department_menu.py
│       ├── appointment_menu.py
│       ├── invoice_menu.py
│       └── report_menu.py
│
├── 📁 tests/
│   ├── __init__.py
│   ├── test_crud.py
│   ├── test_double_booking.py
│   └── test_triggers.py
│
├── 📁 docs/
│   ├── REPORT.docx (20-30 pages)
│   ├── BUSINESS_RULES.md
│   └── DEMO_SCRIPT.md
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🎯 CHECKLIST THEO ĐỀ BÀI (PHẢI CÓ ĐỂ KHÔNG MẤT ĐIỂM)

### Database Design (30%):
- [ ] ERD từ MySQL Workbench
- [ ] 5 bảng đúng yêu cầu đề bài
- [ ] PK, FK, Constraints rõ ràng
- [ ] 5-10 records mỗi bảng

### Advanced Objects (25%):
- [ ] Indexes (ít nhất 2)
- [ ] Views (ít nhất 1 - daily appointments)
- [ ] Stored Procedures (ít nhất 1 - appointment)
- [ ] Functions (ít nhất 1 - billing)
- [ ] Triggers (ít nhất 1 - auto invoice)

### Python Application (20%):
- [ ] Database connection
- [ ] CRUD cho 5 bảng
- [ ] Reports (patient visits + financial)
- [ ] CLI interface

### Security & Admin (15%):
- [ ] User roles + permissions
- [ ] Backup procedure
- [ ] Performance optimization

### Report (10%):
- [ ] 20-30 pages
- [ ] ERD + Screenshots
- [ ] References

---

## ⚡ START NGAY BÂY GIỜ (NGÀY 1)

### Bước 1: Tạo GitHub Repo
```bash
# Tạo repo mới trên GitHub
# Clone về máy
git clone https://github.com/your-team/hospital_management_system.git
cd hospital_management_system
```

### Bước 2: Tạo cấu trúc thư mục
```bash
mkdir -p database/scripts database/diagrams src/models src/repositories src/services src/cli tests docs
```

### Bước 3: Tạo file cơ bản
**requirements.txt:**
```
mysql-connector-python==8.0.33
python-dotenv==1.0.0
tabulate==0.9.0
```

**.env.example:**
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=hospital_db
```

**.gitignore:**
```
__pycache__/
*.pyc
.env
*.md~
*.docx~
database/diagrams/*.mwb
```

### Bước 4: Cài đặt MySQL + Workbench
- Download MySQL 8.0: https://dev.mysql.com/downloads/
- Download Workbench: https://dev.mysql.com/downloads/workbench/

### Bước 5: Test connection
```python
# test_connection.py
import mysql.connector
conn = mysql.connector.connect(host='localhost', user='root', password='your_password')
print("✅ MySQL connected!")
conn.close()
```

---

## 📝 MẪU SQL BẮT ĐẦU (CHO MEMBER 1)

### 01_DDL_Create_DB.sql
```sql
-- =====================================================
-- CREATE DATABASE - HOSPITAL MANAGEMENT SYSTEM
-- Theo đề bài PROJECT 02 - NEU DATCOM Lab
-- =====================================================

DROP DATABASE IF EXISTS hospital_db;
CREATE DATABASE hospital_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE hospital_db;
```

### 02_DDL_Create_Tables.sql
```sql
-- =====================================================
-- CREATE TABLES - 5 BẢNG THEO YÊU CẦU ĐỀ BÀI
-- =====================================================

USE hospital_db;

-- Departments (tạo trước vì các bảng khác reference)
CREATE TABLE Departments (
    DepartmentID VARCHAR(10) PRIMARY KEY,
    DepartmentName VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Patients
CREATE TABLE Patients (
    PatientID VARCHAR(10) PRIMARY KEY,
    PatientName VARCHAR(100) NOT NULL,
    DateOfBirth DATE NOT NULL,
    Gender VARCHAR(1) CHECK (Gender IN ('M', 'F', 'O')),
    Address VARCHAR(255),
    PhoneNumber VARCHAR(15)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Doctors
CREATE TABLE Doctors (
    DoctorID VARCHAR(10) PRIMARY KEY,
    DoctorName VARCHAR(100) NOT NULL,
    DepartmentID VARCHAR(10) NOT NULL,
    Specialty VARCHAR(50),
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Invoices
CREATE TABLE Invoices (
    InvoiceID INT AUTO_INCREMENT PRIMARY KEY,
    PatientID VARCHAR(10) NOT NULL,
    InvoiceDate DATE NOT NULL,
    TotalAmount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Appointments - ⭐ UNIQUE CHỐNG DOUBLE BOOKING
CREATE TABLE Appointments (
    AppointmentID VARCHAR(10) PRIMARY KEY,
    DoctorID VARCHAR(10) NOT NULL,
    PatientID VARCHAR(10) NOT NULL,
    AppointmentDate DATE NOT NULL,
    AppointmentTime TIME NOT NULL,
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    -- Prevent double booking: 1 doctor cannot have 2 appointments at same time
    UNIQUE INDEX idx_doctor_datetime (DoctorID, AppointmentDate, AppointmentTime)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## 🎯 DAILY STANDUP (15 PHÚT - 3 NGÀY/LẦN)

**Mỗi thành viên trả lời 3 câu:**
1. Hôm qua làm được gì?
2. Hôm nay sẽ làm gì?
3. Có block gì không?

**Tools:**
- GitHub Issues để track task
- Discord/Telegram để communicate
- Google Docs để viết report cùng nhau

---

## ⚠️ LƯU Ý QUAN TRỌNG

| Rủi ro | Giải pháp |
|--------|-----------|
| MySQL không install được | Dùng Docker hoặc MySQL online |
| Xung đột Git | Commit nhỏ, pull trước khi push |
| Report không đủ 20 trang | Viết chi tiết mỗi chương, thêm screenshots |
| Code không chạy được | Test từng phần nhỏ, không đợi xong hết mới test |
| Double booking không hoạt động | Test ngay sau khi tạo UNIQUE INDEX |

---

## 📞 HỖ TRỢ TRONG QUÁ TRÌNH LÀM

Nếu gặp vấn đề gì, hỏi ngay:
1. **SQL lỗi** → Gửi error message + code
2. **Python không connect DB** → Gửi config + error
3. **Report không biết viết gì** → Gửi outline chương đó
4. **Git conflict** → Gửi conflict message

---

## ✅ KẾT LUẬN

Với 20 ngày và plan này:
- **Ngày 1-7:** Database xong (30% điểm)
- **Ngày 8-14:** Python xong (20% điểm)
- **Ngày 15-20:** Report + Test xong (50% điểm còn lại)

**Không overengineer - Làm đúng yêu cầu đề bài - Submit đúng hạn**

