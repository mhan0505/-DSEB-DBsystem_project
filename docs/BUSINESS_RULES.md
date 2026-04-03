# BUSINESS RULES - HOSPITAL MANAGEMENT SYSTEM

> Tài liệu này mô tả các quy tắc nghiệp vụ cần implement.
> Sinh viên đọc trước khi code!

---

## 1. ⭐ CHỐNG DOUBLE BOOKING

**Rule:** Một bác sĩ KHÔNG THỂ khám 2 bệnh nhân cùng ngày và giờ.

**Cần implement ở 3 nơi:**
- [ ] SQL: UNIQUE INDEX trên (DoctorID, AppointmentDate, AppointmentTime)
- [ ] Stored Procedure: sp_schedule_appointment check trước khi INSERT
- [ ] Python: AppointmentService.schedule_appointment() gọi check_double_booking()

## 2. ⭐ TỰ ĐỘNG TẠO HÓA ĐƠN

**Rule:** Khi tạo appointment → tự động tạo/cập nhật invoice (50,000 VND).

**Cần implement:**
- [ ] Trigger: trg_after_appointment_insert

## 3. TÍNH TOÁN HÓA ĐƠN

**Rule:** TotalAmount = Số appointment × Phí khám (50,000)

**Cần implement:**
- [ ] Function: fn_calculate_invoice_total

## 4. RÀNG BUỘC DỮ LIỆU

- [ ] Gender chỉ nhận M/F/O (CHECK constraint)
- [ ] TotalAmount >= 0 (Trigger chặn số âm)
- [ ] DepartmentName UNIQUE
- [ ] FK ON DELETE RESTRICT (không xóa dữ liệu đang tham chiếu)

## 5. BÁO CÁO

- [ ] VIEW: vw_daily_appointments
- [ ] VIEW: vw_monthly_revenue
- [ ] VIEW: vw_doctor_appointments
- [ ] VIEW: vw_patient_visit_history
- [ ] VIEW: vw_department_summary

## 6. PHÂN QUYỀN

- [ ] admin_hospital: ALL
- [ ] doctor_user: Read + manage appointments
- [ ] receptionist: CRUD patients + appointments
- [ ] accountant: Manage invoices
- [ ] readonly_user: View only
