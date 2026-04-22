# KỊCH BẢN DEMO - BẢO VỆ ĐỒ ÁN (10 - 15 PHÚT)

> **Mục tiêu:** Chứng minh hệ thống hoàn chỉnh từ Database đến GUI, đáp ứng TẤT CẢ yêu cầu nâng cao của Giảng viên: Phân quyền, Bảo mật, Chống SQL Injection, Chuẩn hóa 3NF, Triggers Tự động hóa và Business Logic.

---

## PHÚT 0-3: CHUẨN BỊ & DEMO PHÂN QUYỀN (RBAC)

**Nói:**
> "Nhóm em xin trình bày Hệ thống Quản lý Bệnh viện. Điểm nhấn của đồ án là giao diện Desktop (GUI) hoàn chỉnh, kết nối trực tiếp với MySQL, và áp dụng chặt chẽ kiến trúc Role-Based Access Control (RBAC)."

**Thao tác Demo:**
1. Chạy lệnh: `python run_gui.py` -> Giao diện Login hiện ra.
2. **Login bằng Kế toán (Accountant):**
   - Click Đăng nhập.
   - **Show:** Giao diện **không có** nút "Đặt lịch khám" và "Quản lý Bệnh nhân".
   - **Show:** Trên Dashboard, ô "Tổng Bác Sĩ" hiện chữ **N/A (màu đỏ)** vì Kế toán bị Database từ chối quyền `SELECT` trên bảng `Doctors`.
   - Click "Đăng xuất".
3. **Login bằng Lễ tân (Receptionist):**
   - Lễ tân có đầy đủ menu để làm việc.

---

## PHÚT 3-5: DEMO QUẢN LÝ BỆNH NHÂN (CRUD & UX)

**Nói:**
> "Ở tính năng Quản lý Bệnh nhân, chúng em chú trọng vào trải nghiệm người dùng (UX) để nhân viên y tế thao tác nhanh và không bị sai sót."

**Thao tác Demo (Quyền Lễ tân):**
1. Vào tab **"👤 Quản lý Bệnh nhân"**.
2. **Tìm kiếm & Auto-fill:** Nhập `P001` vào ô tìm kiếm -> Bấm "Tìm kiếm".
   - **Show:** Dữ liệu bệnh nhân hiện ra ở khung giữa, và form bên dưới **tự động điền (Auto-fill)** thông tin để sẵn sàng chỉnh sửa.
3. Bấm nút **"Làm Mới (Clear)"** màu xám.
   - **Show:** Mọi ô tìm kiếm, text và form đều bị xóa trắng gọn gàng để tránh nhập nhầm đè dữ liệu.
4. **Thêm mới (Lỗi Trùng lặp):** Nhập lại mã `P001`, nhập tên bừa, bấm "Thêm Mới".
   - **Show:** Thay vì văng lỗi mã máy, hệ thống hiện thông báo đỏ tiếng Việt thân thiện: `"🚨 LỖI TRÙNG LẶP: Mã ID hoặc dữ liệu này đã tồn tại..."`.

---

## PHÚT 5-8: DEMO ĐẶT LỊCH & NGHIỆP VỤ (DOUBLE BOOKING)

**Nói:**
> "Để giảm thiểu sai sót (Type Error) khi đặt lịch, giao diện hoàn toàn dùng Hộp thả xuống (Combobox). Đặc biệt, hệ thống có cơ chế chặn Double Booking bằng Business Logic."

**Thao tác Demo:**
1. Vào tab **"📅 Đặt lịch khám"**.
   - **Show:** Mã lịch hẹn (AptID) tự động sinh (chỉ đọc) -> Tránh trùng khóa chính.
   - Chọn Bác sĩ (ví dụ DR001) và Bệnh nhân từ danh sách thả xuống.
   - Chọn Ngày và Giờ thả xuống (VD: `10:00`). Bấm Xác nhận -> **Thành công**.
2. **Cố tình tạo Double Booking:**
   - Đặt tiếp một lịch hẹn khác cho **cùng bác sĩ DR001**, **cùng Ngày** và **cùng Giờ (10:00)**.
   - Bấm Xác nhận -> **Show:** Lỗi nghiệp vụ bị chặn ngay lập tức.

---

## PHÚT 8-10: DEMO TỰ ĐỘNG HÓA TÀI CHÍNH BẰNG TRIGGER

**Nói:**
> "Doanh thu của bệnh viện được tự động hóa hoàn toàn bằng Database-level Logic thông qua Trigger, Python không cần can thiệp."

**Thao tác Demo:**
1. Vào tab **"📋 Tra cứu dữ liệu"**.
2. Chọn **"Báo cáo Doanh thu"** -> Bấm Xem Dữ Liệu.
   - **Show:** Tổng doanh thu hệ thống và danh sách Hóa đơn hiện ra.
3. **Nói & Giải thích:**
   > "Mỗi khi Lễ tân chèn 1 lịch hẹn ở bước trước, Trigger `trg_after_appointment_insert` dưới Database sẽ tự động 'cò súng', tự chèn một hóa đơn 50.000 VNĐ vào bảng Invoices. Nếu bệnh nhân khám 2 lần trong 1 ngày, Trigger sẽ thông minh cộng dồn tiền vào hóa đơn cũ. Đảm bảo toàn vẹn tài chính tuyệt đối."

---

## PHÚT 10-12: DEMO BẢO MẬT (ENCRYPTION & SQL INJECTION)

**Nói:**
> "Hệ thống sở hữu lớp bảo mật sâu. Bao gồm mã hóa AES-256 Fernet và Input Validation."

**Thao tác Demo:**
1. Trở lại tab **"Quản lý Bệnh nhân"**, thử tấn công SQL Injection vào ô Tìm kiếm:
   - Nhập: `' OR 1=1; DROP TABLE Patients;--`
   - Bấm Tìm kiếm -> **Show:** Hệ thống báo lỗi Validation, chặn ngay các ký tự bất hợp pháp.
2. Mở MySQL Workbench (hoặc chạy lệnh SQL trực tiếp):
   ```sql
   SELECT PatientName, PhoneNumber, Address FROM Patients LIMIT 3;
   ```
   - **Show:** Số điện thoại và Địa chỉ đang hiển thị chuỗi loằng ngoằng `gAAAAA...`.
   - **Giải thích:** "Dữ liệu nhạy cảm đã bị mã hóa 2 chiều trước khi lưu. Chỉ khi hiển thị lên GUI mới được giải mã, giúp chống lộ lọt thông tin khi DB bị hack."

**KẾT THÚC DEMO.**
> "Đồ án của chúng em không chỉ dừng ở mức ứng dụng CRUD cơ bản, mà còn triển khai các kỹ thuật thao tác Database nâng cao. Cảm ơn thầy cô đã lắng nghe."
