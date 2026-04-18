# KỊCH BẢN DEMO - 5 PHÚT
## Hospital Management System (Business Logic Focus)

> **Mục tiêu:** Chứng minh hệ thống có BUSINESS LOGIC thật, không chỉ CRUD đơn giản.  
> **Thời gian:** 5 phút  
> **Focus:** Double booking prevention, Triggers, Procedures, Reports

---

## CHUẨN BỊ TRƯỚC DEMO

```bash
# 1. Đảm bảo database đã chạy
mysql -u root -p hospital_db

# 2. Chạy ứng dụng Python
cd -DSEB-DBsystem_project
python -m src.cli.main
```

---

## PHÚT 0-1: GIỚI THIỆU HỆ THỐNG

**Nói:**
> "Hệ thống quản lý bệnh viện với 5 bảng theo yêu cầu đề bài.
> Điểm đặc biệt: hệ thống có business logic thật - ngăn chặn double booking,
> tự động tạo hóa đơn, và báo cáo thống kê."

**Show:**
- ER Diagram từ MySQL Workbench
- 5 bảng: Departments, Patients, Doctors, Appointments, Invoices
- **Nhấn mạnh:** UNIQUE INDEX `idx_doctor_datetime`

---

## PHÚT 1-2: ⭐ DEMO DOUBLE BOOKING PREVENTION

**Nói:**
> "Quy tắc quan trọng nhất: một bác sĩ không thể khám 2 bệnh nhân cùng giờ."

**Demo trong CLI:**
```
Menu → 4. Appointment Management → 3. Schedule New Appointment

# Lần 1: Đặt lịch thành công
Appointment ID: DEMO01
Doctor ID: DR001
Patient ID: P001
Date: 2025-06-15
Time: 10:00:00
→ ✅ SUCCESS: Appointment scheduled

# Lần 2: CÙNG bác sĩ, CÙNG giờ → BỊ CHẶN
Appointment ID: DEMO02
Doctor ID: DR001
Patient ID: P002
Date: 2025-06-15
Time: 10:00:00
→ ❌ ERROR: DOUBLE BOOKING - Doctor DR001 already has appointment at this time
```

**Nói:**
> "Hệ thống chặn ở 3 lớp: Python check trước, Stored Procedure check giữa,
> UNIQUE INDEX chặn cuối cùng ở database level."

---

## PHÚT 2-3: ⭐ DEMO TRIGGER TỰ ĐỘNG

**Demo trong MySQL:**
```sql
-- Kiểm tra invoice TRƯỚC khi tạo appointment
SELECT * FROM Invoices WHERE PatientID = 'P009';
-- → (empty hoặc ít records)

-- Tạo appointment mới
INSERT INTO Appointments (AppointmentID, DoctorID, PatientID, AppointmentDate, AppointmentTime)
VALUES ('DEMO03', 'DR003', 'P009', '2025-06-20', '14:00:00');

-- Kiểm tra invoice SAU → tự động tạo!
SELECT * FROM Invoices WHERE PatientID = 'P009' AND InvoiceDate = '2025-06-20';
-- → ✅ Invoice tự động tạo với TotalAmount = 50,000 VND
```

**Nói:**
> "Trigger `trg_after_appointment_insert` tự động tạo hóa đơn.
> Không cần INSERT thủ công vào bảng Invoices."

---

## PHÚT 3-4: ⭐ DEMO STORED PROCEDURE + FUNCTION

**Demo Procedure:**
```sql
-- Schedule qua stored procedure
CALL sp_schedule_appointment('DEMO04', 'DR001', 'P003', '2025-06-15', '11:00:00', @status, @msg);
SELECT @status AS Status, @msg AS Message;
-- → SUCCESS: Appointment scheduled successfully

-- Thử double booking qua procedure
CALL sp_schedule_appointment('DEMO05', 'DR001', 'P004', '2025-06-15', '11:00:00', @status, @msg);
SELECT @status AS Status, @msg AS Message;
-- → ERROR: DOUBLE BOOKING
```

**Demo Function:**
```sql
-- Tính tuổi bệnh nhân
SELECT PatientName, fn_get_patient_age(PatientID) AS Age FROM Patients LIMIT 5;

-- Tính tổng chi tiêu
SELECT PatientName, fn_get_patient_total_spent(PatientID) AS TotalSpent FROM Patients LIMIT 5;
```

---

## PHÚT 4-5: ⭐ DEMO REPORTS

**Demo trong CLI:**
```
Menu → 6. Reports & Statistics

# Report 1: Monthly Revenue
→ Show bảng doanh thu theo tháng

# Report 2: Doctor Performance
→ Show số lượt khám theo bác sĩ

# Report 3: Patient Visit History
→ Show lịch sử khám + tổng chi tiêu

# Report 4: System Dashboard
→ Show tổng quan hệ thống
```

**Nói:**
> "Tất cả reports sử dụng VIEWs được tạo sẵn trong database,
> đảm bảo performance và dữ liệu luôn cập nhật."

---

## KẾT LUẬN (30 giây)

**Nói:**
> "Hệ thống Hospital Management không chỉ là CRUD đơn giản. Chúng tôi đã implement:
> 1. **Double booking prevention** - 3 lớp bảo vệ
> 2. **Auto invoice trigger** - tự động tạo hóa đơn
> 3. **Stored procedures** - tự động hóa nghiệp vụ
> 4. **UDF functions** - tính toán billing
> 5. **5 Views** - báo cáo Patient visits + Financial
> 6. **5 User roles** - phân quyền bảo mật
>
> Tất cả theo đúng yêu cầu đề bài DATCOM Lab."

---

## CLEANUP SAU DEMO

```sql
-- Xóa dữ liệu demo
DELETE FROM Appointments WHERE AppointmentID LIKE 'DEMO%';
DELETE FROM Invoices WHERE PatientID IN (
    SELECT PatientID FROM Appointments WHERE AppointmentID LIKE 'DEMO%'
);
```
