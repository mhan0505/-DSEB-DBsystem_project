# DÀN Ý THUYẾT TRÌNH: PHÂN QUYỀN VÀ BẢO MẬT HỆ THỐNG QUẢN LÝ BỆNH VIỆN

## Phần 1: Mở đầu & Tư duy bảo mật của hệ thống
* **Vấn đề đặt ra:** Dữ liệu y tế là dữ liệu cực kỳ nhạy cảm. Việc rò rỉ thông tin hoặc bị phá hoại cơ sở dữ liệu sẽ gây hậu quả nghiêm trọng.
* **Giải pháp tiếp cận:** Hệ thống áp dụng mô hình bảo mật nhiều lớp (Defense in Depth) trải dài từ tầng Ứng dụng (Python/GUI) cho tới tầng Cơ sở dữ liệu (MySQL).
* **3 Cột mốc bảo mật chính:** Phân quyền chặt chẽ (RBAC) - Mã hóa & Ghi vết (Encryption & Auditing) - Chống tấn công (Anti SQL-Injection).

---

## Phần 2: Phân quyền người dùng (Role-Based Access Control)
*Điểm nhấn: Nguyên tắc Đặc quyền tối thiểu (Principle of Least Privilege).*
Thay vì sử dụng một tài khoản root chung cho cả ứng dụng, hệ thống chia nhỏ quyền hạn thành **5 Roles** riêng biệt trực tiếp trên MySQL (`09_Security_Users.sql`):
1. **`admin_hospital`**: Có toàn quyền trên database (Full Access).
2. **`doctor_user`**: Chỉ được phép xem danh sách bệnh nhân, xem và cập nhật lịch hẹn của mình. Gọi được một số thủ tục nhất định (`sp_schedule_appointment`).
3. **`receptionist`**: Lễ tân có quyền Thêm/Sửa thông tin bệnh nhân và Quản lý toàn bộ lịch hẹn.
4. **`accountant`**: Kế toán chỉ có quyền xem lịch hẹn/bệnh nhân để Thêm/Sửa Hóa đơn và gọi các thủ tục báo cáo doanh thu (`sp_generate_invoice`).
5. **`readonly_user`**: Quyền chỉ đọc trên toàn hệ thống (dành cho kiểm toán viên).
* **Kết luận phần này:** Bất kể hệ thống GUI có bị hack, hacker cũng không thể xóa dữ liệu (DROP, DELETE) nếu họ đang dùng tài khoản của bác sĩ hay kế toán.

---

## Phần 3: Mã hóa dữ liệu nhạy cảm (Data Encryption)
*Điểm nhấn: Bảo vệ dữ liệu ngay cả khi database bị lộ.*
* **Phương pháp:** Mã hóa cấp độ Database (Database-level Encryption).
* **Triển khai:** 
  * Sử dụng thuật toán mã hóa mạnh **AES (Advanced Encryption Standard)** với Secret Key.
  * Đã tự định nghĩa các hàm `fn_encrypt_data` và `fn_decrypt_data` (`10_Data_Encryption.sql`) để mã hóa các trường thông tin nhạy cảm (ví dụ: Số điện thoại, thông tin liên lạc).
* **Kết luận phần này:** Nếu ai đó truy cập trực tiếp vào bảng bệnh nhân mà không có quyền giải mã, họ chỉ thấy các chuỗi ký tự vô nghĩa (VARBINARY).

---

## Phần 4: Nhật ký hệ thống và Kiểm toán (Audit Logging)
*Điểm nhấn: Trách nhiệm giải trình (Accountability).*
* **Cơ chế:** Sử dụng bảng `AuditLogs` để ghi lại **mọi sự thay đổi** dữ liệu.
* **Tự động hóa bằng Trigger:** 
  * Hệ thống cài đặt các Database Triggers chạy ngầm (`11_Audit_Logging.sql`).
  * Bất cứ khi nào có lệnh `INSERT`, `UPDATE` hoặc `DELETE` trên các bảng quan trọng (như *Patients*, *Appointments*), Trigger sẽ tự động ghi lại:
    * **Ai** là người thực hiện (`USER()`)
    * **Hành động gì** (`ActionType`)
    * **Lúc nào** (`LogTimestamp`)
    * **Chi tiết** ra sao.
* **Kết quả:** Admin có thể dễ dàng truy vết thông qua View `vw_system_audit` nếu có dữ liệu bị xóa sai hoặc thay đổi bất thường.

---

## Phần 5: Chống tấn công SQL Injection (Application Layer)
*Điểm nhấn: Bảo vệ từ "Cửa khẩu".*
Bảo mật không chỉ ở Database mà còn ở code Python (`src/security/input_validator.py`). Hệ thống có 3 lớp khiên chắn:
1. **Parameterized Queries:** Mọi thao tác gọi xuống Database đều được tham số hóa, không ghép chuỗi bừa bãi.
2. **Whitelist Validation:** Kiểm tra đầu vào cực kỳ khắt khe. 
   * ID chỉ được chứa chữ và số.
   * Ngày tháng phải chuẩn `YYYY-MM-DD`.
   * Tự động phát hiện và chặn các từ khóa nguy hiểm (`UNION`, `SELECT`, `--`, `;`).
3. **Che giấu lỗi (Sanitize Error Messages):** Nếu có lỗi SQL xảy ra (VD: lỗi cú pháp), hệ thống sẽ bắt lỗi, ghi log nội bộ và chỉ hiển thị "Lỗi hệ thống" ra ngoài cho người dùng. Tuyệt đối **không** tiết lộ cấu trúc bảng, tên cột cho kẻ tấn công thấy.

---

## Phần 6: Tổng kết
* Hệ thống Quản lý Bệnh viện không chỉ đáp ứng tốt các nghiệp vụ y tế, mà còn là một hệ thống **an toàn và đáng tin cậy**.
* Tuân thủ tiêu chuẩn an toàn thông tin cơ bản: Tính bảo mật (Confidentiality) - Tính toàn vẹn (Integrity) - Tính sẵn sàng (Availability).
