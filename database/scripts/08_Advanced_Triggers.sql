-- =====================================================
-- SCRIPT 08: TRIGGERS - TỰ ĐỘNG HÓA NGHIỆP VỤ
-- Hospital Management System - NEU DATCOM Lab
-- Theo yêu cầu: "Automatically update related data
--   when new appointments or invoices are added"
-- =====================================================

USE hospital_db;

DROP TRIGGER IF EXISTS trg_after_appointment_insert;
DROP TRIGGER IF EXISTS trg_before_appointment_insert;
DROP TRIGGER IF EXISTS trg_after_appointment_delete;
DROP TRIGGER IF EXISTS trg_before_invoice_insert;

DELIMITER $$

-- =====================================================
-- ⭐ TRIGGER 1: Tự động tạo/cập nhật invoice khi có appointment mới
-- Event: AFTER INSERT ON Appointments
-- Logic:
--   1. Check if invoice exists for this patient on this date
--   2. If NO  → CREATE new invoice (50,000 VND)
--   3. If YES → UPDATE existing invoice (add 50,000 VND)
--
-- TODO: Implement this trigger
-- HINT: Use NEW.PatientID and NEW.AppointmentDate to access inserted row
-- HINT: DECLARE v_invoice_exists INT; SELECT COUNT(*) INTO ...
-- HINT: Use IF/ELSE for create vs update logic
-- =====================================================
CREATE TRIGGER trg_after_appointment_insert
AFTER INSERT ON Appointments
FOR EACH ROW
BEGIN
    -- TODO: Declare variables
    -- DECLARE v_invoice_exists INT DEFAULT 0;
    -- DECLARE v_invoice_id VARCHAR(10);
    -- DECLARE v_consultation_fee DECIMAL(10,2) DEFAULT 50000.00;

    -- TODO: Check if invoice exists for NEW.PatientID on NEW.AppointmentDate

    -- TODO: IF not exists → INSERT new invoice

    -- TODO: ELSE → UPDATE existing invoice (add fee)

    SELECT 1; -- placeholder, remove when implementing
END$$

-- =====================================================
-- TRIGGER 2: Validate appointment data before insert
-- Event: BEFORE INSERT ON Appointments
-- TODO: Check that AppointmentDate and AppointmentTime are NOT NULL
-- HINT: Use SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '...' to raise error
-- =====================================================
CREATE TRIGGER trg_before_appointment_insert
BEFORE INSERT ON Appointments
FOR EACH ROW
BEGIN
    -- TODO: Validate NEW.AppointmentDate IS NOT NULL
    -- TODO: Validate NEW.AppointmentTime IS NOT NULL
    -- HINT: IF NEW.AppointmentDate IS NULL THEN
    --         SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Date cannot be NULL';
    --       END IF;

    SELECT 1; -- placeholder
END$$

-- =====================================================
-- TRIGGER 3: Adjust invoice when appointment is deleted
-- Event: AFTER DELETE ON Appointments
-- TODO: When appointment is deleted:
--   - If invoice amount <= consultation fee → DELETE the invoice
--   - If invoice amount > consultation fee → SUBTRACT the fee
-- HINT: Use OLD.PatientID and OLD.AppointmentDate
-- =====================================================
CREATE TRIGGER trg_after_appointment_delete
AFTER DELETE ON Appointments
FOR EACH ROW
BEGIN
    -- TODO: Get current invoice amount
    -- TODO: If only 1 appointment → delete invoice
    -- TODO: If multiple appointments → subtract fee

    SELECT 1; -- placeholder
END$$

-- =====================================================
-- TRIGGER 4: Validate invoice amount before insert
-- Event: BEFORE INSERT ON Invoices
-- TODO: Block negative TotalAmount
-- HINT: IF NEW.TotalAmount < 0 THEN SIGNAL ...
-- =====================================================
CREATE TRIGGER trg_before_invoice_insert
BEFORE INSERT ON Invoices
FOR EACH ROW
BEGIN
    -- TODO: Check NEW.TotalAmount >= 0
    -- If negative → SIGNAL error

    SELECT 1; -- placeholder
END$$

DELIMITER ;

-- VERIFY
SHOW TRIGGERS FROM hospital_db;
