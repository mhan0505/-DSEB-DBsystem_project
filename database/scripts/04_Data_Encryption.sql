USE hospital_db;

-- 2. Tạo Function mã hóa
DROP FUNCTION IF EXISTS fn_encrypt_data;
DELIMITER $$
CREATE FUNCTION fn_encrypt_data(p_data VARCHAR(255)) 
RETURNS VARBINARY(512) 
DETERMINISTIC 
BEGIN 
    RETURN AES_ENCRYPT(p_data, @db_encryption_key);
END $$
DELIMITER ;

-- 3. Tạo Function giải mã
DROP FUNCTION IF EXISTS fn_decrypt_data;
DELIMITER $$
CREATE FUNCTION fn_decrypt_data(p_encrypted VARBINARY(512)) 
RETURNS VARCHAR(255) 
DETERMINISTIC 
BEGIN 
    RETURN CAST(AES_DECRYPT(p_encrypted, @db_encryption_key) AS CHAR);
END $$
DELIMITER ;

-- 4. Cấp quyền
GRANT EXECUTE ON FUNCTION hospital_db.fn_encrypt_data TO 'admin_hospital'@'localhost', 'receptionist'@'localhost', 'doctor_user'@'localhost';
GRANT EXECUTE ON FUNCTION hospital_db.fn_decrypt_data TO 'admin_hospital'@'localhost', 'receptionist'@'localhost', 'doctor_user'@'localhost';
