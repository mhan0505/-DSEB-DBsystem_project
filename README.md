<<<<<<< Updated upstream
# 🏥 Hospital Management System - LEARNING VERSION

> **🎯 Phiên bản TODO để sinh viên tự implement**  
> Tham khảo bản đầy đủ tại: `hospital_management_system/`

---

## ⚠️ HƯỚNG DẪN SỬ DỤNG

Đây là bản **LEARNING** - code đã được loại bỏ phần logic, chỉ giữ lại:
- ✅ Cấu trúc folder
- ✅ Class và function signatures
- ✅ Imports
- ✅ TODO comments hướng dẫn chi tiết
- ❌ Logic / SQL queries (sinh viên tự viết)

## 📚 THỨ TỰ IMPLEMENT (khuyến nghị)

### Phase 1: Database (Tuần 0.5)
1. `database/scripts/01_DDL_Create_DB.sql` - Tạo database
2. `database/scripts/02_DDL_Create_Tables.sql` - ⭐ 5 bảng + UNIQUE INDEX
3. `database/scripts/03_DML_Insert_Data.sql` - Dữ liệu mẫu

### Phase 2: Python Foundation (Tuần 1)
4. `src/config.py` - Cấu hình kết nối (chỉ cần đổi password)
5. `src/database_connection.py` - ⭐ Kết nối MySQL
6. `src/models/*.py` - 5 data models (to_dict, from_dict)

### Phase 3: CRUD (Tuần 1.5)
7. `src/repositories/patient_repository.py` - Start here (simplest)
8. `src/repositories/department_repository.py`
9. `src/repositories/doctor_repository.py`
10. `src/repositories/appointment_repository.py` - ⭐ check_double_booking
11. `src/repositories/invoice_repository.py`

### Phase 4: Business Logic (Tuần 2)
12. `src/services/appointment_service.py` - ⭐ Double booking prevention
13. `src/services/invoice_service.py`

### Phase 5: Advanced SQL (Tuần 2.5)
14. `database/scripts/04_Advanced_Indexes.sql`
15. `database/scripts/05_Advanced_Views.sql` - ⭐ 5 views
16. `database/scripts/06_Advanced_Procedures.sql` - ⭐ Stored procedures
17. `database/scripts/07_Advanced_Functions.sql` - UDFs
18. `database/scripts/08_Advanced_Triggers.sql` - ⭐ Auto invoice

### Phase 6: CLI + Reports (Tuần 3)
19. `src/cli/main.py` - Main menu
20. `src/cli/report_menu.py` - 7 reports

### Phase 7: Testing + Security (Tuần 3)
21. `tests/test_double_booking.py` - ⭐ Most important test
22. `tests/test_triggers.py`
23. `tests/test_stored_procedures.py`
24. `tests/test_crud_real.py`
25. `database/scripts/09_Security_Users.sql`

## 💡 TIPS

- Bắt đầu từ **Patient** (đơn giản nhất) rồi áp dụng pattern tương tự cho Doctor, Department
- Luôn **test từng bước** - đừng viết hết rồi mới chạy
- Khi gặp lỗi FK constraint → kiểm tra thứ tự INSERT (Departments trước, rồi Doctors)
- Tham khảo bản đầy đủ tại `../hospital_management_system/` khi bị stuck
- 📖 Đọc [HUONG_DAN_GIT.md](HUONG_DAN_GIT.md) nếu chưa biết dùng Git!

---

## 👥 PHÂN CÔNG NHÓM

| Thành viên | Vai trò | Branch | Phụ trách | Deadline |
|---|---|---|---|---|
| 🔵 **Duy Anh** | DB Foundation | `duyanh-database` | Scripts 01-03 (Tạo DB, Tables, Data) + ERD | Tuần 0.5 |
| 🟢 **Nguyen Duc** | Advanced SQL | `nguyenduc-advanced-sql` | Scripts 04-08 (Indexes, Views, Procs, Funcs, Triggers) | Tuần 2.5 |
| 🟡 **Tran Tuan Minh** | Python Core | `tuanminh-python-core` | `src/config.py`, `database_connection.py`, `models/`, `repositories/` | Tuần 1.5 |
| 🟠 **Duc Duy** | CLI & Reports | `ducduy-cli-reports` | `src/cli/main.py`, `src/cli/report_menu.py` | Tuần 3 |
| 🔴 **Lead (mhan0505)** ⭐ | Business Logic + QA | `lead-services-tests` | `src/services/` ⭐, `tests/` ⭐, Security, Docs, Review & Merge | Ongoing |

### Chi tiết từng người:

**🔵 Duy Anh — DB Foundation (Tuần 0.5)**
- `01_DDL_Create_DB.sql` — Tạo database hospital_db
- `02_DDL_Create_Tables.sql` — 5 bảng + ⭐ UNIQUE INDEX chống double booking
- `03_DML_Insert_Data.sql` — 5-10 bản ghi mỗi bảng (tên VN)
- Tạo ERD diagram trong MySQL Workbench

**🟢 Nguyen Duc — Advanced SQL (Tuần 2.5)**
- `04_Advanced_Indexes.sql` — 10 performance indexes
- `05_Advanced_Views.sql` — 5 views cho reports
- `06_Advanced_Procedures.sql` — 5 stored procedures (⭐ sp_schedule_appointment)
- `07_Advanced_Functions.sql` — 4 UDFs (⭐ fn_calculate_invoice_total)
- `08_Advanced_Triggers.sql` — 4 triggers (⭐ trg_after_appointment_insert)
> ⚠️ Phải đợi **Duy Anh** xong Phase 1 trước!

**🟡 Tran Tuan Minh — Python Core (Tuần 1.5)**
- `src/config.py` — Cấu hình kết nối MySQL
- `src/database_connection.py` — Singleton + context manager
- `src/models/*.py` — 5 dataclass models (to_dict, from_dict)
- `src/repositories/*.py` — CRUD cho 5 bảng + ⭐ check_double_booking()
> ⚠️ Phải đợi **Duy Anh** tạo tables trước khi test!

**🟠 Duc Duy — CLI & Reports (Tuần 3)**
- `src/cli/main.py` — Menu chính: Patient, Doctor, Dept, Appointment, Invoice
- `src/cli/report_menu.py` — 7 loại reports (daily, monthly, doctor, patient, dept, financial, dashboard)
> ⚠️ Phải đợi **Tuan Minh** hoàn thành repositories!

**🔴 Lead (mhan0505) — Business Logic + QA ⭐ (Ongoing)**
- `src/services/appointment_service.py` — ⭐ Logic chống double booking (3 lớp)
- `src/services/invoice_service.py` — ⭐ Tính tiền + gọi UDF
- `tests/test_double_booking.py` — ⭐ Test quan trọng nhất
- `tests/test_triggers.py`, `test_stored_procedures.py`, `test_crud_real.py`
- `database/scripts/09_Security_Users.sql` — 5 user roles
- `docs/` — Business Rules, Demo Script, Report Outline
- **Review & Merge** tất cả Pull Requests
- **Integration testing** — đảm bảo toàn hệ thống chạy đúng

### Thứ tự phụ thuộc:

```
Duy Anh (DB Foundation)
    ↓
Nguyen Duc (Advanced SQL)  +  Tuan Minh (Python Core)
    ↓                              ↓
    └──────────┬───────────────────┘
               ↓
        Lead (Services + Tests)
               ↓
        Duc Duy (CLI + Reports)
```

### Bắt đầu:
=======
# Hospital Management System
**NEU DATCOM Lab - Database Management System Project**

---

## Giới thiệu

Hệ thống quản lý bệnh viện xây dựng trên MySQL + Python CLI, bao gồm:
- 5 bảng: Departments, Patients, Doctors, Appointments, Invoices
- Chống double booking (3 lớp bảo vệ)
- Tự động tạo hóa đơn qua Trigger
- Stored Procedures, UDFs, Views, Indexes
- Phân quyền 5 user roles
- CLI interface + 7 loại báo cáo

---

## Cài đặt

>>>>>>> Stashed changes
```bash
git clone https://github.com/mhan0505/-DSEB-DBsystem_project.git
cd -DSEB-DBsystem_project
pip install -r requirements.txt
cp .env.example .env        # Sửa DB_PASSWORD trong .env
```

Chạy SQL scripts theo thứ tự:
```
database/scripts/01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09
```

Chạy ứng dụng:
```bash
python -m src.cli.main
```

---

## Cấu trúc project

```
-DSEB-DBsystem_project/
├── database/scripts/       # SQL: DDL, DML, Indexes, Views, Procedures, Triggers, Security
├── src/
│   ├── config.py           # Cấu hình DB (đọc từ .env)
│   ├── database_connection.py
│   ├── models/             # Patient, Doctor, Department, Appointment, Invoice
│   ├── repositories/       # CRUD cho 5 bảng
│   ├── services/           # Business logic (double booking, invoice)
│   └── cli/                # main.py + report_menu.py
├── tests/                  # test_double_booking, test_triggers, test_stored_procedures, test_crud
├── docs/                   # BUSINESS_RULES, DEMO_SCRIPT, REPORT_OUTLINE
├── .env.example
└── requirements.txt
```

---

## Phân công nhóm

| Thành viên | Vai trò | Branch | Phụ trách |
|---|---|---|---|
| Duy Anh | DB Foundation | `duyanh-database` | Scripts 01-03, ERD |
| Nguyen Duc | Advanced SQL | `nguyenduc-advanced-sql` | Scripts 04-08 |
| Tran Tuan Minh | Python Core | `tuanminh-python-core` | models/, repositories/ |
| Duc Duy | CLI & Reports | `ducduy-cli-reports` | src/cli/ |
| mhan0505 (Lead) | Business Logic + QA | `lead-services-tests` | services/, tests/, docs/, review |

---

## Tính năng nổi bật

**Double booking prevention (3 lớp):**
1. Python: `AppointmentService.check_double_booking()`
2. Stored Procedure: `sp_schedule_appointment`
3. Database: `UNIQUE INDEX idx_doctor_datetime`

**Auto invoice trigger:**
- `trg_after_appointment_insert` tự tạo/cập nhật hóa đơn 50,000 VND mỗi lượt khám

**5 Views báo cáo:**
- `vw_daily_appointments`, `vw_monthly_revenue`, `vw_doctor_appointments`, `vw_patient_visit_history`, `vw_department_summary`

---

## Chạy tests

```bash
python -m pytest tests/ -v
```
