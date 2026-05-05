# KẾ HOẠCH TRIỂN KHAI BẢO MẬT HỆ THỐNG (TỔNG HỢP)

Dưới đây là lộ trình 4 bước để hoàn thiện phần Bảo mật và Phân quyền cho dự án của bạn.

## Bước 1: Cập nhật cấu trúc bảng (DDL)
Chỉnh sửa file `02_DDL_Create_Tables.sql` để cột chứa dữ liệu nhạy cảm có thể lưu trữ mã nhị phân.

```sql
-- Trong bảng Patients
ALTER TABLE Patients MODIFY COLUMN PhoneNumber VARBINARY(512);
-- Tương tự cho cột Address nếu bạn muốn mã hóa cả địa chỉ
ALTER TABLE Patients MODIFY COLUMN Address VARBINARY(512);
```

## Bước 2: Cài đặt Hàm mã hóa & Giải mã
Chạy file `10_Data_Encryption.sql`. Hãy đảm bảo Key mã hóa được giữ bí mật.

```sql
-- Hàm mã hóa
CREATE FUNCTION fn_encrypt_data(p_data VARCHAR(255)) RETURNS VARBINARY(512) ...
-- Hàm giải mã
CREATE FUNCTION fn_decrypt_data(p_encrypted VARBINARY(512)) RETURNS VARCHAR(255) ...
```

## Bước 3: Tự động hóa bằng Triggers
Tạo các Trigger để việc mã hóa diễn ra âm thầm, giúp code Python của bạn đơn giản hơn (chỉ cần gửi văn bản thuần xuống DB).

```sql
-- Trigger cho INSERT
DELIMITER $$
CREATE TRIGGER trg_encrypt_patient_phone_before_insert
BEFORE INSERT ON Patients FOR EACH ROW
BEGIN
    IF NEW.PhoneNumber IS NOT NULL THEN
        SET NEW.PhoneNumber = fn_encrypt_data(NEW.PhoneNumber);
    END IF;
END$$

-- Trigger cho UPDATE
CREATE TRIGGER trg_encrypt_patient_phone_before_update
BEFORE UPDATE ON Patients FOR EACH ROW
BEGIN
    -- Chỉ mã hóa lại nếu dữ liệu mới khác dữ liệu cũ (đã giải mã)
    IF NEW.PhoneNumber <> OLD.PhoneNumber THEN
        SET NEW.PhoneNumber = fn_encrypt_data(NEW.PhoneNumber);
    END IF;
END$$
DELIMITER ;
```

## Bước 4: Tạo View và Phân quyền (Security Layer)
Đây là bước quan trọng nhất để bác sĩ vẫn xem được dữ liệu mà hacker thì không.

### 4.1. Tạo View dành cho người có quyền
```sql
CREATE VIEW vw_patient_authorized_details AS
SELECT 
    PatientID, 
    PatientName, 
    DateOfBirth,
    Gender,
    fn_decrypt_data(Address) AS Address,
    fn_decrypt_data(PhoneNumber) AS PhoneNumber
FROM Patients;
```

### 4.2. Cập nhật file phân quyền (09_Security_Users.sql)
```sql
-- Bác sĩ & Lễ tân: Xem qua VIEW (Thấy dữ liệu thật)
GRANT SELECT ON hospital_db.vw_patient_authorized_details TO 'doctor_user'@'localhost';
GRANT SELECT ON hospital_db.vw_patient_authorized_details TO 'receptionist'@'localhost';

-- Kế toán/Admin: Chỉ xem qua TABLE gốc (Thấy dữ liệu đã mã hóa)
GRANT SELECT ON hospital_db.Patients TO 'accountant'@'localhost';
```

---
## Lợi ích sau khi sửa đổi:
1.  **Dữ liệu "Chết":** Nếu ai đó copy file database ra ngoài, họ không có Key giải mã nên dữ liệu hoàn toàn vô dụng.
2.  **Trong suốt (Transparency):** Code Python của bạn không cần quan tâm đến việc mã hóa. Bạn cứ INSERT số điện thoại bình thường, Database tự lo.
3.  **Kiểm soát chặt:** Bạn có thể quyết định chính xác AI được xem số điện thoại thật thông qua việc cấp quyền trên View.
