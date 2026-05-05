-- =====================================================
-- SCRIPT 11: AUDIT LOGGING & SYSTEM AUDIT
-- Hospital Management System - NEU DATCOM Lab
-- Yêu cầu: "Quản lý, phân quyền và kiểm soát người dùng"
-- =====================================================

USE hospital_db;

-- 1. Tạo bảng AuditLog để theo dõi mọi thay đổi dữ liệu
CREATE TABLE IF NOT EXISTS AuditLogs (
    LogID INT AUTO_INCREMENT PRIMARY KEY,
    TableName VARCHAR(50),
    ActionType ENUM('INSERT', 'UPDATE', 'DELETE'),
    RecordID VARCHAR(20),
    PerformedBy VARCHAR(100),    -- User thực hiện (ví dụ: 'receptionist@localhost')
    LogTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Details TEXT                 -- Mô tả chi tiết (ví dụ: 'Updated Phone Number')
);

-- 2. Trigger ghi log cho bảng Patients (Theo dõi thay đổi thông tin PII)
DELIMITER $$

DROP TRIGGER IF EXISTS trg_audit_patient_insert$$
CREATE TRIGGER trg_audit_patient_insert
AFTER INSERT ON Patients
FOR EACH ROW
BEGIN
    INSERT INTO AuditLogs (TableName, ActionType, RecordID, PerformedBy, Details)
    VALUES ('Patients', 'INSERT', NEW.PatientID, USER(), 
            CONCAT('New patient added: ', NEW.PatientName));
END$$

DROP TRIGGER IF EXISTS trg_audit_patient_update$$
CREATE TRIGGER trg_audit_patient_update
AFTER UPDATE ON Patients
FOR EACH ROW
BEGIN
    INSERT INTO AuditLogs (TableName, ActionType, RecordID, PerformedBy, Details)
    VALUES ('Patients', 'UPDATE', NEW.PatientID, USER(), 
            CONCAT('Updated patient details for: ', NEW.PatientName));
END$$

DROP TRIGGER IF EXISTS trg_audit_patient_delete$$
CREATE TRIGGER trg_audit_patient_delete
AFTER DELETE ON Patients
FOR EACH ROW
BEGIN
    INSERT INTO AuditLogs (TableName, ActionType, RecordID, PerformedBy, Details)
    VALUES ('Patients', 'DELETE', OLD.PatientID, USER(), 
            CONCAT('Removed patient: ', OLD.PatientName));
END$$

-- 3. Trigger ghi log cho bảng Appointments (Theo dõi lịch hẹn)
DROP TRIGGER IF EXISTS trg_audit_appointment_insert$$
CREATE TRIGGER trg_audit_appointment_insert
AFTER INSERT ON Appointments
FOR EACH ROW
BEGIN
    INSERT INTO AuditLogs (TableName, ActionType, RecordID, PerformedBy, Details)
    VALUES ('Appointments', 'INSERT', NEW.AppointmentID, USER(), 
            CONCAT('Scheduled appointment for Patient: ', NEW.PatientID, ' with Doctor: ', NEW.DoctorID));
END$$

DELIMITER ;

-- 4. View dành cho Admin để kiểm tra lịch sử truy cập hệ thống
CREATE OR REPLACE VIEW vw_system_audit AS
SELECT 
    LogID, 
    LogTimestamp, 
    PerformedBy, 
    ActionType, 
    TableName, 
    RecordID, 
    Details
FROM AuditLogs
ORDER BY LogTimestamp DESC;

-- 5. Cấp quyền cho các Role liên quan đến Audit
-- Chỉ Admin mới được xem Audit Log đầy đủ
GRANT SELECT ON hospital_db.AuditLogs TO 'admin_hospital'@'localhost';
GRANT SELECT ON hospital_db.vw_system_audit TO 'admin_hospital'@'localhost';

-- Role readonly_user có thể được xem để phục vụ kiểm toán
GRANT SELECT ON hospital_db.vw_system_audit TO 'readonly_user'@'localhost';

SELECT 'Audit logging system configured successfully!' AS Status;
