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
