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
DROP TRIGGER IF EXISTS trg_encrypt_patient_phone_before_insert;
DROP TRIGGER IF EXISTS trg_encrypt_patient_phone_before_update;

DELIMITER $$

-- =====================================================
-- ⭐ TRIGGER 1: Tự động tạo/cập nhật invoice khi có appointment mới
-- Event: AFTER INSERT ON Appointments
-- =====================================================
CREATE TRIGGER trg_after_appointment_insert
AFTER INSERT ON Appointments
FOR EACH ROW
BEGIN
    DECLARE v_invoice_exists INT DEFAULT 0;
    DECLARE v_invoice_id VARCHAR(10);
    DECLARE v_consultation_fee DECIMAL(10, 2) DEFAULT 50000.00;

    -- 1. Kiểm tra xem hóa đơn đã tồn tại chưa
    SELECT COUNT(*) INTO v_invoice_exists
    FROM Invoices
    WHERE PatientID = NEW.PatientID
      AND InvoiceDate = NEW.AppointmentDate;

    -- 2. Xử lý Logic tạo mới hoặc cập nhật
    IF v_invoice_exists = 0 THEN
        -- Tạo mã hóa đơn: I + yymmdd + 3 số ngẫu nhiên
        SET v_invoice_id = CONCAT(
            'I',
            DATE_FORMAT(NEW.AppointmentDate, '%y%m%d'),
            LPAD(FLOOR(RAND() * 1000), 3, '0')
        );

        INSERT INTO Invoices (InvoiceID, PatientID, InvoiceDate, TotalAmount)
        VALUES (
            v_invoice_id,
            NEW.PatientID,
            NEW.AppointmentDate,
            v_consultation_fee
        );
    ELSE
        -- Cập nhật cộng thêm phí
        UPDATE Invoices
        SET TotalAmount = TotalAmount + v_consultation_fee
        WHERE PatientID = NEW.PatientID
          AND InvoiceDate = NEW.AppointmentDate;
    END IF;
END $$

-- =====================================================
-- TRIGGER 2: Validate appointment data before insert
-- Event: BEFORE INSERT ON Appointments
-- =====================================================
CREATE TRIGGER trg_before_appointment_insert
BEFORE INSERT ON Appointments
FOR EACH ROW
BEGIN
    -- Kiểm tra ngày không được trống
    IF NEW.AppointmentDate IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Appointment date cannot be NULL';
    END IF;

    -- Kiểm tra giờ không được trống
    IF NEW.AppointmentTime IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Appointment time cannot be NULL';
    END IF;
END $$

-- =====================================================
-- TRIGGER 3: Adjust invoice when appointment is deleted
-- Event: AFTER DELETE ON Appointments
-- =====================================================
CREATE TRIGGER trg_after_appointment_delete
AFTER DELETE ON Appointments
FOR EACH ROW
BEGIN
    DECLARE v_current_amount DECIMAL(10, 2) DEFAULT 0.00;
    DECLARE v_consultation_fee DECIMAL(10, 2) DEFAULT 50000.00;

    -- Lấy số tiền hiện tại
    SELECT TotalAmount INTO v_current_amount
    FROM Invoices
    WHERE PatientID = OLD.PatientID
      AND InvoiceDate = OLD.AppointmentDate;

    IF v_current_amount <= v_consultation_fee THEN
        -- Xóa hóa đơn nếu không còn phí khác
        DELETE FROM Invoices
        WHERE PatientID = OLD.PatientID
          AND InvoiceDate = OLD.AppointmentDate;
    ELSE
        -- Trừ phí nếu vẫn còn các lịch hẹn khác
        UPDATE Invoices
        SET TotalAmount = TotalAmount - v_consultation_fee
        WHERE PatientID = OLD.PatientID
          AND InvoiceDate = OLD.AppointmentDate;
    END IF;
END $$

-- =====================================================
-- TRIGGER 4: Validate invoice amount before insert
-- Event: BEFORE INSERT ON Invoices
-- =====================================================
CREATE TRIGGER trg_before_invoice_insert
BEFORE INSERT ON Invoices
FOR EACH ROW
BEGIN
    -- Không cho phép số tiền âm
    IF NEW.TotalAmount < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invoice total amount cannot be negative';
    END IF;
END $$

-- =====================================================
-- TRIGGER 5: Tự động mã hóa dữ liệu nhạy cảm trước khi lưu
-- Event: BEFORE INSERT ON Patients
-- =====================================================
CREATE TRIGGER trg_encrypt_patient_phone_before_insert
BEFORE INSERT ON Patients
FOR EACH ROW
BEGIN
    -- Mã hóa Số điện thoại
    IF NEW.PhoneNumber IS NOT NULL THEN
        SET NEW.PhoneNumber = fn_encrypt_data(NEW.PhoneNumber);
    END IF;

    -- Mã hóa Địa chỉ
    IF NEW.Address IS NOT NULL THEN
        SET NEW.Address = fn_encrypt_data(NEW.Address);
    END IF;
END $$

-- =====================================================
-- TRIGGER 6: Tự động mã hóa lại dữ liệu khi cập nhật
-- Event: BEFORE UPDATE ON Patients
-- =====================================================
CREATE TRIGGER trg_encrypt_patient_phone_before_update
BEFORE UPDATE ON Patients
FOR EACH ROW
BEGIN
    -- Mã hóa lại Số điện thoại nếu thay đổi
    IF NEW.PhoneNumber <> OLD.PhoneNumber THEN
        SET NEW.PhoneNumber = fn_encrypt_data(NEW.PhoneNumber);
    END IF;

    -- Mã hóa lại Địa chỉ nếu thay đổi
    IF NEW.Address <> OLD.Address THEN
        SET NEW.Address = fn_encrypt_data(NEW.Address);
    END IF;
END $$

DELIMITER ;

-- =====================================================
-- VERIFY
-- =====================================================
SHOW TRIGGERS FROM hospital_db;