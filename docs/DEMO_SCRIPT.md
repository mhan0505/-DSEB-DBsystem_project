# KỊCH BẢN DEMO - BẢO VỆ ĐỒ ÁN (10 PHÚT)

> **Mục tiêu:** Chứng minh hệ thống hoàn chỉnh từ Database đến GUI, đáp ứng TẤT CẢ yêu cầu nâng cao của Giảng viên: Phân quyền, Bảo mật, Chống SQL Injection, Chuẩn hóa 3NF và Business Logic.

---

## PHÚT 0-2: CHUẨN BỊ & GIỚI THIỆU TỔNG QUAN

**Nói:**
> "Nhóm em xin trình bày Hệ thống Quản lý Bệnh viện. Điểm nhấn của đồ án là chúng em đã xây dựng một giao diện Desktop (GUI) hoàn chỉnh, kết nối trực tiếp với MySQL, và implement đầy đủ các lớp bảo mật, phân quyền theo yêu cầu của thầy/cô."

**Show:**
- Mở Terminal/CMD, chạy lệnh: `python run_gui.py`
- Giao diện Login hiện ra.
- Chỉ vào tài liệu **[NORMALIZATION_3NF.md](NORMALIZATION_3NF.md)** để chứng minh Database 5 bảng đã đạt chuẩn 3NF.

---

## PHÚT 2-4: DEMO PHÂN QUYỀN (RBAC & LEAST PRIVILEGE)

**Nói:**
> "Hệ thống áp dụng Role-Based Access Control. Tùy vào tài khoản đăng nhập mà giao diện và quyền truy cập dữ liệu sẽ khác nhau."

**Thao tác Demo:**
1. **Login bằng Kế toán (Accountant)**
   - Ở Dropdown chọn "Kế toán (Accountant)" -> Click Đăng nhập.
   - **Show:** Giao diện **không có** nút "Đặt lịch khám".
   - **Show:** Trên Dashboard, ô "Tổng Bác Sĩ" hiện chữ **N/A (màu đỏ)** vì Kế toán bị Database từ chối quyền `SELECT` trên bảng `Doctors`.
   - Click "Đăng xuất".

2. **Login bằng Lễ tân (Receptionist)**
   - Ở Dropdown chọn "Lễ tân (Receptionist)" -> Click Đăng nhập.
   - **Show:** Nút "Đặt lịch khám" hiện ra.
   - **Show:** Ô "Tổng Bác Sĩ" hiện số liệu bình thường vì Lễ tân được quyền xem bảng này.

---

## PHÚT 4-6: DEMO CHỐNG SQL INJECTION (3 LỚP)

**Nói:**
> "Để bảo vệ Database, hệ thống có 3 lớp chống SQL Injection: Input Validation ở tầng Python, Parameterized Queries ở Repository, và Quyền hạn hạn chế ở MySQL."

**Thao tác Demo (Đang ở quyền Lễ tân):**
1. Vào tab **"Đặt Lịch Khám"**.
2. Thử tấn công SQL Injection:
   - Mục **Mã Bệnh Nhân (Pat ID)** nhập mã độc: `' OR 1=1`
   - Nhập bừa các trường khác.
   - Bấm **"Xác nhận Đặt Lịch"**.
   - **Show:** Popup hiện thông báo đỏ chặn ngay lập tức: `Lỗi Validation: ... bị chặn bởi Input Validator`.

3. Thử kiểu phá cấu trúc:
   - Mục **Mã Lịch Hẹn** nhập: `APT; DROP TABLE Patients;--`
   - Bấm Xác nhận.
   - **Show:** Bị chặn ngay lập tức vì sai định dạng.

**Nói:**
> "Tất cả các truy vấn xuống Database đều dùng `(%s)` parameterized, nên dù hacker có vượt qua được Validation thì mã SQL độc hại cũng chỉ được coi là Text thông thường, không thể thực thi."

---

## PHÚT 6-8: DEMO BUSINESS LOGIC (DOUBLE BOOKING)

**Nói:**
> "Về nghiệp vụ, quy tắc quan trọng nhất là một bác sĩ không thể khám 2 bệnh nhân cùng giờ."

**Thao tác Demo:**
1. Đặt lịch lần 1 (Hợp lệ):
   - Apt ID: `DEMO001`
   - Doc ID: `DR001`
   - Pat ID: `P001`
   - Date: `2026-10-10`
   - Time: `10:00:00`
   - Click Xác nhận -> **Show:** Thông báo xanh thành công.

2. Đặt lịch lần 2 (Trùng lịch bác sĩ DR001):
   - Apt ID: `DEMO002`
   - Doc ID: `DR001` (vẫn bác sĩ này)
   - Pat ID: `P002` (bệnh nhân khác)
   - Date: `2026-10-10` (cùng ngày)
   - Time: `10:00:00` (cùng giờ)
   - Click Xác nhận -> **Show:** Thông báo lỗi màu đỏ từ Business Logic: `"Doctor DR001 already has appointment at this time"`.

---

## PHÚT 8-10: DEMO MÃ HÓA (ENCRYPTION) & AUDIT LOG

**Nói:**
> "Cuối cùng là bảo mật dữ liệu nhạy cảm PII và giám sát hệ thống."

**Thao tác Demo:**
1. Mở MySQL Workbench (hoặc chạy câu lệnh SQL):
   ```sql
   USE hospital_db;
   SELECT PatientName, PhoneNumber, Address FROM Patients LIMIT 3;
   ```
   - **Show:** Số điện thoại và địa chỉ trong DB đang là các chuỗi loằng ngoằng (gAAAAA...). Chứng minh dữ liệu đã bị mã hóa **AES-256 Fernet** trước khi lưu.
   
2. Truy vết Audit Log:
   ```sql
   SELECT * FROM vw_system_audit LIMIT 5;
   ```
   - **Show:** Bảng Log ghi nhận vừa có tài khoản `receptionist@localhost` gọi lệnh `INSERT` để tạo lịch hẹn `DEMO001` lúc mấy giờ. Chứng tỏ hệ thống lưu lại mọi vết tích sửa đổi dữ liệu!

**KẾT THÚC DEMO.**
> "Cảm ơn thầy/cô đã theo dõi. Đồ án của chúng em không chỉ hoàn thành phần CRUD cơ bản mà còn đảm bảo tính toàn vẹn nghiệp vụ và an toàn thông tin chuyên sâu."
