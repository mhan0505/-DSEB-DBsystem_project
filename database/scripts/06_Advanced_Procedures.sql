-- =====================================================
-- SCRIPT 06: STORED PROCEDURES
-- Hospital Management System - NEU DATCOM Lab
-- Theo yêu cầu: "Automate operations such as
--   appointment management and invoice generation"
-- =====================================================

USE hospital_db;

DROP PROCEDURE IF EXISTS sp_schedule_appointment;
DROP PROCEDURE IF EXISTS sp_generate_invoice;
DROP PROCEDURE IF EXISTS sp_cancel_appointment;
DROP PROCEDURE IF EXISTS sp_get_patient_history;
DROP PROCEDURE IF EXISTS sp_daily_report;

DELIMITER $$

-- =====================================================
-- ⭐ PROCEDURE 1: Đặt lịch hẹn (có check double booking)
-- This is the MOST IMPORTANT procedure!
--
-- Parameters:
--   IN  p_AppointmentID  VARCHAR(10)
--   IN  p_DoctorID       VARCHAR(10)
--   IN  p_PatientID      VARCHAR(10)
--   IN  p_AppointmentDate DATE
--   IN  p_AppointmentTime TIME
--   OUT p_Status          VARCHAR(50)   → 'SUCCESS' or 'ERROR'
--   OUT p_Message         VARCHAR(255)  → description
--
-- TODO: Implement the following logic:
--   1. DECLARE variables for validation checks
--   2. Check if doctor exists (SELECT COUNT INTO variable)
--   3. Check if patient exists
--   4. ⭐ Check for DOUBLE BOOKING: same doctor + date + time
--   5. IF any check fails → SET p_Status = 'ERROR' with message
--   6. IF all pass → INSERT INTO Appointments and SET p_Status = 'SUCCESS'
--
-- BONUS: Add EXIT HANDLER FOR 1062 (duplicate key) as backup safety
-- =====================================================
CREATE PROCEDURE sp_schedule_appointment(
    IN p_AppointmentID  VARCHAR(10),
    IN p_DoctorID       VARCHAR(10),
    IN p_PatientID      VARCHAR(10),
    IN p_AppointmentDate DATE,
    IN p_AppointmentTime TIME,
    OUT p_Status        VARCHAR(50),
    OUT p_Message       VARCHAR(255)
)
BEGIN
    -- TODO: Declare validation variables
    -- HINT: DECLARE v_doctor_exists INT DEFAULT 0;

    -- TODO: Check doctor exists
    -- HINT: SELECT COUNT(*) INTO v_doctor_exists FROM Doctors WHERE DoctorID = p_DoctorID;

    -- TODO: Check patient exists

    -- TODO: ⭐ Check double booking
    -- HINT: SELECT COUNT(*) INTO v_double_booking FROM Appointments
    --       WHERE DoctorID = p_DoctorID AND AppointmentDate = p_AppointmentDate
    --       AND AppointmentTime = p_AppointmentTime;

    -- TODO: Validate with IF/ELSEIF
    -- If doctor not found → ERROR
    -- If patient not found → ERROR
    -- If double booking → ERROR with 'DOUBLE BOOKING' message
    -- Else → INSERT and SUCCESS

    SET p_Status = 'ERROR';
    SET p_Message = 'Not yet implemented';
END$$

-- =====================================================
-- ⭐ PROCEDURE 2: Tạo hóa đơn
-- TODO: Create procedure sp_generate_invoice
-- Parameters: IN invoice_id, patient_id, date, amount; OUT status, message
-- Logic: validate patient exists, amount >= 0, then INSERT
-- =====================================================
CREATE PROCEDURE sp_generate_invoice(
    IN p_InvoiceID      VARCHAR(10),
    IN p_PatientID      VARCHAR(10),
    IN p_InvoiceDate    DATE,
    IN p_TotalAmount    DECIMAL(10, 2),
    OUT p_Status        VARCHAR(50),
    OUT p_Message       VARCHAR(255)
)
BEGIN
    -- TODO: Check patient exists
    -- TODO: Check amount >= 0
    -- TODO: INSERT INTO Invoices
    -- TODO: SET status and message

    SET p_Status = 'ERROR';
    SET p_Message = 'Not yet implemented';
END$$

-- =====================================================
-- PROCEDURE 3: Hủy lịch hẹn
-- TODO: Create procedure sp_cancel_appointment
-- Parameters: IN appointment_id; OUT status, message
-- Logic: check appointment exists, get details, then DELETE
-- =====================================================
CREATE PROCEDURE sp_cancel_appointment(
    IN p_AppointmentID  VARCHAR(10),
    OUT p_Status        VARCHAR(50),
    OUT p_Message       VARCHAR(255)
)
BEGIN
    -- TODO: Check appointment exists
    -- TODO: DELETE FROM Appointments
    -- TODO: SET status and message

    SET p_Status = 'ERROR';
    SET p_Message = 'Not yet implemented';
END$$

-- =====================================================
-- PROCEDURE 4: Lịch sử khám bệnh nhân
-- TODO: Create procedure sp_get_patient_history
-- Should return: patient info, appointment list, invoice list
-- HINT: A procedure can have multiple SELECT statements
-- =====================================================
CREATE PROCEDURE sp_get_patient_history(
    IN p_PatientID VARCHAR(10)
)
BEGIN
    -- TODO: SELECT patient information

    -- TODO: SELECT appointment history (JOIN with Doctors, Departments)
    -- ORDER BY AppointmentDate DESC

    -- TODO: SELECT invoice history
    -- ORDER BY InvoiceDate DESC

    SELECT 'Not yet implemented' AS Status;
END$$

-- =====================================================
-- PROCEDURE 5: Báo cáo tổng hợp theo ngày
-- TODO: Create procedure sp_daily_report
-- Should return: summary (counts, revenue) + appointment details + invoice details
-- =====================================================
CREATE PROCEDURE sp_daily_report(
    IN p_ReportDate DATE
)
BEGIN
    -- TODO: Summary: total appointments, total invoices, total revenue for the date

    -- TODO: Appointment details for the date

    -- TODO: Invoice details for the date

    SELECT 'Not yet implemented' AS Status;
END$$

DELIMITER ;

-- =====================================================
-- VERIFY
-- =====================================================
SHOW PROCEDURE STATUS WHERE Db = 'hospital_db';
