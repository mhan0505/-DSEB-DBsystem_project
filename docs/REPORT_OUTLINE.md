# BÁO CÁO PROJECT - OUTLINE (20-30 trang)
## Hospital Management System

> **Theo chuẩn báo cáo NEU DATCOM Lab**  
> **Target pages:** 20-30 trang

---

## MỤC LỤC

### PHẦN 1: TỔNG QUAN (3-4 trang)

**1.1. Giới thiệu đề tài** (1 trang)
- Bối cảnh: số hóa quản lý bệnh viện
- Mục tiêu dự án
- Phạm vi hệ thống

**1.2. Công nghệ sử dụng** (0.5 trang)
- MySQL 8.0 (Database)
- Python 3.x (Application)
- mysql-connector-python (Database connector)

**1.3. Phân công công việc** (0.5 trang)
- Bảng phân công theo thành viên
- Timeline thực hiện

**1.4. Quy tắc nghiệp vụ (Business Rules)** (1-2 trang)
- ⭐ Chống double booking
- ⭐ Tự động tạo hóa đơn
- Ràng buộc dữ liệu
- Phân quyền người dùng

---

### PHẦN 2: THIẾT KẾ CƠ SỞ DỮ LIỆU (5-7 trang)

**2.1. ER Diagram** (1-2 trang)
- ER Diagram từ MySQL Workbench (ảnh)
- Giải thích các thực thể và quan hệ

**2.2. Database Schema** (2-3 trang)
- Bảng Departments: cấu trúc, PK
- Bảng Patients: cấu trúc, PK, CHECK constraint
- Bảng Doctors: cấu trúc, PK, FK → Departments
- Bảng Invoices: cấu trúc, PK, FK → Patients
- Bảng Appointments: cấu trúc, PK, FK × 2, ⭐ UNIQUE INDEX

**2.3. Quan hệ giữa các bảng** (1 trang)
- Departments ←1:N→ Doctors
- Patients ←1:N→ Appointments ←N:1→ Doctors
- Patients ←1:N→ Invoices
- Database Diagram (ảnh)

**2.4. Dữ liệu mẫu** (1 trang)
- Mỗi bảng 5-10 bản ghi
- Ảnh chụp kết quả SELECT

---

### PHẦN 3: CÁC ĐỐI TƯỢNG NÂNG CAO (6-8 trang)

**3.1. Indexes** (1 trang)
- UNIQUE INDEX idx_doctor_datetime (business rule)
- Performance indexes: idx_patient_name, idx_appointment_date, ...
- Giải thích lý do chọn index

**3.2. Views** (1-2 trang)
- vw_daily_appointments: lịch hẹn hôm nay
- vw_monthly_revenue: doanh thu tháng
- vw_doctor_appointments: thống kê bác sĩ
- vw_patient_visit_history: lịch sử khám
- vw_department_summary: thống kê khoa
- Ảnh chụp kết quả SELECT từ views

**3.3. Stored Procedures** (1-2 trang)
- ⭐ sp_schedule_appointment: đặt lịch + check double booking
- sp_generate_invoice: tạo hóa đơn
- sp_cancel_appointment: hủy lịch hẹn
- sp_get_patient_history: lịch sử bệnh nhân
- sp_daily_report: báo cáo ngày
- Ảnh chụp CALL procedure + kết quả

**3.4. User Defined Functions** (1 trang)
- ⭐ fn_calculate_invoice_total: tính tiền hóa đơn
- fn_get_patient_age: tính tuổi
- fn_get_doctor_appointment_count: đếm lượt khám
- fn_get_patient_total_spent: tổng chi tiêu
- Ảnh chụp SELECT với function

**3.5. Triggers** (1-2 trang)
- ⭐ trg_after_appointment_insert: tự tạo invoice
- trg_before_appointment_insert: validate dữ liệu
- trg_after_appointment_delete: cập nhật invoice khi xóa
- trg_before_invoice_insert: chặn số âm
- Ảnh chụp BEFORE/AFTER trigger firing

---

### PHẦN 4: ỨNG DỤNG PYTHON (3-4 trang)

**4.1. Kiến trúc ứng dụng** (1 trang)
- Mô hình 3 lớp: Models → Repositories → Services
- Sơ đồ kiến trúc
- Database Connection (Singleton pattern)

**4.2. CRUD Operations** (1 trang)
- Create / Read / Update / Delete cho 5 bảng
- Ảnh chụp CLI interface

**4.3. Business Logic Layer** (1 trang)
- ⭐ AppointmentService: check double booking ở Python
- InvoiceService: tính toán hóa đơn
- Ảnh chụp double booking bị chặn

**4.4. Reports** (1 trang)
- Daily Appointments Report
- Monthly Revenue Report
- Doctor Performance Report
- Patient Visit History
- System Dashboard
- Ảnh chụp output reports

---

### PHẦN 5: BẢO MẬT & QUẢN TRỊ (2-3 trang)

**5.1. Phân quyền người dùng** (1 trang)
- 5 roles: admin, doctor, receptionist, accountant, readonly
- Bảng quyền chi tiết
- GRANT/REVOKE statements

**5.2. Bảo mật dữ liệu** (0.5 trang)
- Password hashing
- Prepared statements (chống SQL injection)
- Input validation

**5.3. Backup & Recovery** (0.5 trang)
- mysqldump command
- Lịch backup tự động
- Quy trình khôi phục

**5.4. Tối ưu hiệu năng** (1 trang)
- Index strategy
- Query optimization
- EXPLAIN ANALYZE cho queries quan trọng

---

### PHẦN 6: TESTING (1-2 trang)

**6.1. Test Cases** (1 trang)
- ⭐ test_double_booking.py: 4 test cases
- test_triggers.py: 3 test cases
- test_stored_procedures.py: 3 test cases
- test_crud_real.py: 7 test cases

**6.2. Kết quả test** (0.5 trang)
- Ảnh chụp unittest output
- Tất cả tests PASS

---

### PHẦN 7: KẾT LUẬN (1-2 trang)

**7.1. Kết quả đạt được**
- Hoàn thành 5 bảng theo yêu cầu
- Implement đầy đủ advanced objects
- Business logic hoạt động đúng
- Reports theo yêu cầu: Patient visits + Financial

**7.2. Hạn chế**
- Chưa có GUI (chỉ CLI)
- Chưa tích hợp bảo hiểm y tế
- Phí khám cố định (chưa theo chuyên khoa)

**7.3. Hướng phát triển**
- Thêm GUI (Tkinter/Web)
- Tích hợp bảo hiểm
- Phí khám theo chuyên khoa
- Hệ thống nhắc lịch hẹn

---

### PHỤ LỤC

**A. Toàn bộ SQL Scripts** (tham chiếu file)
**B. Python Source Code** (tham chiếu file)
**C. Test Results**

---

## CHECKLIST TRƯỚC KHI NỘP

- [ ] Bìa + Mục lục
- [ ] ER Diagram (ảnh từ MySQL Workbench)
- [ ] Database Diagram (ảnh từ Workbench)
- [ ] Ảnh chụp kết quả query (SELECT từ views)
- [ ] Ảnh chụp CLI hoạt động
- [ ] Ảnh chụp double booking bị chặn
- [ ] Ảnh chụp trigger tự tạo invoice
- [ ] Ảnh chụp test results (all PASS)
- [ ] Review: 20-30 trang
- [ ] Kiểm tra format theo chuẩn trường NEU
