-- =====================================================
-- SCRIPT 10: DATABASE-LEVEL DATA ENCRYPTION
-- Hospital Management System - NEU DATCOM Lab
-- Yêu cầu: "Bảo mật/mã hóa dữ liệu nhạy cảm"
-- =====================================================

USE hospital_db;

-- 1. Cấu hình Key mã hóa cho Database (Chỉ Admin mới biết)
-- Trong thực tế, key này nên được quản lý bởi Key Management System
SET @key_str = 'hospital_secret_key_2024';

-- 2. Tạo Function để mã hóa dữ liệu (Encryption)
-- Sử dụng thuật toán AES (Advanced Encryption Standard)
DROP FUNCTION IF EXISTS fn_encrypt_data;
DELIMITER $$
CREATE FUNCTION fn_encrypt_data(p_data VARCHAR(255)) 
RETURNS VARBINARY(512)
DETERMINISTIC
BEGIN
    RETURN AES_ENCRYPT(p_data, 'hospital_secret_key_2024');
END$$
DELIMITER ;

-- 3. Tạo Function để giải mã dữ liệu (Decryption)
DROP FUNCTION IF EXISTS fn_decrypt_data;
DELIMITER $$
CREATE FUNCTION fn_decrypt_data(p_encrypted VARBINARY(512)) 
RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
    RETURN CAST(AES_DECRYPT(p_encrypted, 'hospital_secret_key_2024') AS CHAR);
END$$
DELIMITER ;

-- 4. Ví dụ cách sử dụng trong SQL:
-- SELECT PatientName, fn_decrypt_data(PhoneNumber) FROM Patients;

-- 5. Cấp quyền sử dụng hàm
-- Mọi user đều có thể dùng hàm để đọc dữ liệu (nếu họ có quyền SELECT trên bảng)
GRANT EXECUTE ON FUNCTION hospital_db.fn_encrypt_data TO 'admin_hospital'@'localhost';
GRANT EXECUTE ON FUNCTION hospital_db.fn_decrypt_data TO 'admin_hospital'@'localhost';

SELECT 'Database-level encryption functions created successfully!' AS Status;
