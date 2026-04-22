# BUSINESS RULES - HOSPITAL MANAGEMENT SYSTEM

> **Project:** Hospital Management System  
> **Course:** Database Management System - NEU DATCOM Lab  
> **Version:** 1.0

---

## QUY TẮC NGHIỆP VỤ CỐT LÕI

### 1. ⭐ CHỐNG DOUBLE BOOKING (Quan trọng nhất)

**Rule:** Một bác sĩ KHÔNG THỂ khám 2 bệnh nhân cùng ngày và giờ.

**Lý do:** Trong thực tế, một bác sĩ chỉ có thể tiếp một bệnh nhân tại một thời điểm. Vi phạm quy tắc này sẽ gây ra:
- Xung đột lịch hẹn
- Bệnh nhân phải chờ đợi không cần thiết
- Giảm chất lượng dịch vụ

**Implementation (3 lớp bảo vệ):**

| Layer | Mechanism | File |
|-------|-----------|------|
| Database | `UNIQUE INDEX idx_doctor_datetime (DoctorID, AppointmentDate, AppointmentTime)` | `02_DDL_Create_Tables.sql` |
| Stored Procedure | `sp_schedule_appointment` check COUNT trước khi INSERT | `06_Advanced_Procedures.sql` |
| Python Application | `AppointmentService.schedule_appointment()` gọi `check_double_booking()` | `appointment_service.py` |

**Test:** `tests/test_double_booking.py`
- `test_01_double_booking_prevented_by_unique_index` - Core test
- `test_02_same_doctor_different_time_allowed` - Cùng BS khác giờ → OK
- `test_03_different_doctor_same_time_allowed` - Khác BS cùng giờ → OK
- `test_04_same_doctor_different_date_allowed` - Cùng BS khác ngày → OK

---

### 2. ⭐ TỰ ĐỘNG TẠO HÓA ĐƠN (Auto Invoice)

**Rule:** Mỗi khi có appointment mới → hệ thống tự động tạo hoặc cập nhật invoice.

**Chi tiết:**
- Nếu bệnh nhân **chưa có** invoice trong ngày → **Tạo invoice mới** với phí khám cơ bản
- Nếu bệnh nhân **đã có** invoice trong ngày → **Cộng thêm** phí khám vào invoice hiện tại
- Phí khám cơ bản: **50,000 VND / lượt**

**Implementation:**
- Trigger: `trg_after_appointment_insert` (AFTER INSERT ON Appointments)
- File: `08_Advanced_Triggers.sql`

**Test:** `tests/test_triggers.py`
- `test_01_trigger_creates_invoice_on_new_appointment`
- `test_02_trigger_updates_invoice_on_second_appointment`

---

### 3. ⭐ TÍNH TOÁN HÓA ĐƠN (Invoice Calculation)

**Rule:** `TotalAmount = Số lượt appointment trong ngày × Phí khám cơ bản`

**Mở rộng (tương lai):**
- Phí khám chuyên khoa (cao hơn phí thường)
- Giảm giá cho bệnh nhân thường xuyên
- Bảo hiểm y tế

**Implementation:**
- UDF: `fn_calculate_invoice_total(PatientID, InvoiceDate)`
- File: `07_Advanced_Functions.sql`

---

### 4. RÀNG BUỘC DỮ LIỆU (Data Constraints)

| Constraint | Bảng | Mô tả |
|------------|------|--------|
| Gender CHECK | Patients | Chỉ nhận 'M', 'F', 'O' |
| TotalAmount >= 0 | Invoices | Trigger chặn số âm |
| DepartmentName UNIQUE | Departments | Không trùng tên khoa |
| FK ON DELETE RESTRICT | Doctors, Appointments, Invoices | Không xóa dữ liệu đang tham chiếu |
| FK ON UPDATE CASCADE | All FK tables | Tự động cập nhật khi đổi ID |

---

### 5. ⭐ BÁO CÁO (Reports)

Theo yêu cầu đề bài: **Patient visits** + **Financial transactions**

| Report | View/Source | Mô tả |
|--------|------------|--------|
| Daily Appointments | `vw_daily_appointments` | Lịch hẹn hôm nay |
| Monthly Revenue | `vw_monthly_revenue` | Doanh thu theo tháng |
| Doctor Performance | `vw_doctor_appointments` | Số lượt khám theo BS |
| Patient Visit History | `vw_patient_visit_history` | Lịch sử khám + chi tiêu |
| Department Summary | `vw_department_summary` | Thống kê theo khoa |

**Implementation:** `src/cli/report_menu.py`

---

### 6. PHÂN QUYỀN NGƯỜI DÙNG (Security)

| Role | Quyền | Bảng truy cập |
|------|-------|---------------|
| `admin_hospital` | ALL PRIVILEGES | Tất cả |
| `doctor_user` | SELECT + INSERT/UPDATE Appointments | Patients, Doctors, Appointments |
| `receptionist` | CRUD Patients + Appointments | Patients, Appointments |
| `accountant` | SELECT + Manage Invoices | Invoices, Financial Views |
| `readonly_user` | SELECT only | Tất cả (chỉ đọc) |

**Implementation:** `09_Security_Users.sql`

---

### 7. AUTO-ADJUST ON DELETE

**Rule:** Khi xóa appointment → tự động giảm tiền invoice tương ứng.

- Nếu invoice chỉ còn 1 appointment → **xóa invoice**
- Nếu invoice có nhiều appointment → **giảm phí khám**

**Implementation:** Trigger `trg_after_appointment_delete`

---

## TỔNG KẾT LUỒNG NGHIỆP VỤ

```
Patient đăng ký → Đặt lịch hẹn (check double booking)
                       ↓
              Appointment được tạo
                       ↓
              Trigger tự tạo/update Invoice
                       ↓
              Báo cáo: Visits + Financial
```
