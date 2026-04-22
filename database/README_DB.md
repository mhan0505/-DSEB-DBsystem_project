# 🗄️ Database - Hospital Management System

## Cách chạy SQL Scripts (theo thứ tự)

```bash
# 1. Tạo database
mysql -u root -p < scripts/01_DDL_Create_DB.sql

# 2. Tạo bảng (với UNIQUE INDEX chống double booking)
mysql -u root -p < scripts/02_DDL_Create_Tables.sql

# 3. Insert dữ liệu mẫu
mysql -u root -p < scripts/03_DML_Insert_Data.sql

# 4. Tạo indexes
mysql -u root -p < scripts/04_Advanced_Indexes.sql

# 5. Tạo views
mysql -u root -p < scripts/05_Advanced_Views.sql

# 6. Tạo stored procedures
mysql -u root -p < scripts/06_Advanced_Procedures.sql

# 7. Tạo functions
mysql -u root -p < scripts/07_Advanced_Functions.sql

# 8. Tạo triggers
mysql -u root -p < scripts/08_Advanced_Triggers.sql

# 9. Cấu hình bảo mật (Roles & Permissions)
mysql -u root -p < scripts/09_Security_Users.sql

# 10. Mã hóa dữ liệu (Encryption)
mysql -u root -p < scripts/10_Data_Encryption.sql

# 11. Hệ thống giám sát (Audit Logging)
mysql -u root -p < scripts/11_Audit_Logging.sql
```

## Hoặc chạy tất cả cùng lúc

```bash
mysql -u root -p < scripts/01_DDL_Create_DB.sql && \
mysql -u root -p hospital_db < scripts/02_DDL_Create_Tables.sql && \
mysql -u root -p hospital_db < scripts/03_DML_Insert_Data.sql && \
mysql -u root -p hospital_db < scripts/04_Advanced_Indexes.sql && \
mysql -u root -p hospital_db < scripts/05_Advanced_Views.sql && \
mysql -u root -p hospital_db < scripts/06_Advanced_Procedures.sql && \
mysql -u root -p hospital_db < scripts/07_Advanced_Functions.sql && \
mysql -u root -p hospital_db < scripts/08_Advanced_Triggers.sql && \
mysql -u root -p hospital_db < scripts/09_Security_Users.sql && \
mysql -u root -p hospital_db < scripts/11_Audit_Logging.sql
```

## ERD Diagram

File: `diagrams/ERD_Workbench.png` (tạo từ MySQL Workbench)

### Quan hệ giữa các bảng:
- `Departments` ←1—N→ `Doctors`
- `Patients` ←1—N→ `Appointments` ←N—1→ `Doctors`
- `Patients` ←1—N→ `Invoices`

## ⭐ Business Rules

1. **Double Booking Prevention**: UNIQUE INDEX `idx_doctor_datetime` trên `(DoctorID, AppointmentDate, AppointmentTime)`
2. **Auto Invoice**: Trigger `trg_after_appointment_insert` tự tạo invoice khi có appointment mới
3. **Invoice Validation**: Trigger `trg_before_invoice_insert` đảm bảo `TotalAmount >= 0`
4. **Audit Trail**: Hệ thống Audit Log ghi lại mọi thao tác của người dùng (`INSERT/UPDATE/DELETE`)
5. **Data Encryption**: Mã hóa PII (PhoneNumber, Address) bằng AES-256 ở tầng Application.

Mở MySQL Workbench.
Vào Database -> Reverse Engineer.
Chọn connection local của bạn.
Tick schema hospital_db.
Finish để Workbench sinh EER Diagram từ DB hiện tại.
File -> Export -> PNG/SVG và lưu vào database/diagrams.