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
    DECLARE v_doctor_exists INT DEFAULT 0;
    DECLARE v_patient_exists INT DEFAULT 0;
    DECLARE v_double_booking INT DEFAULT 0;

    -- TODO: Check doctor exists
    -- HINT: SELECT COUNT(*) INTO v_doctor_exists FROM Doctors WHERE DoctorID = p_DoctorID;
    SELECT COUNT(*) INTO v_doctor_exists
    FROM Doctors
    WHERE DoctorID = (p_DoctorID COLLATE utf8mb4_unicode_ci);

    -- TODO: Check patient exists
    SELECT COUNT(*) INTO v_patient_exists
    FROM Patients
    WHERE PatientID = (p_PatientID COLLATE utf8mb4_unicode_ci);

    -- TODO: ⭐ Check double booking
    -- HINT: SELECT COUNT(*) INTO v_double_booking FROM Appointments
    --       WHERE DoctorID = p_DoctorID AND AppointmentDate = p_AppointmentDate
    --       AND AppointmentTime = p_AppointmentTime;
        SELECT COUNT(*) INTO v_double_booking
        FROM Appointments
        WHERE DoctorID = (p_DoctorID COLLATE utf8mb4_unicode_ci)
            AND AppointmentDate = p_AppointmentDate
            AND AppointmentTime = p_AppointmentTime;

    -- TODO: Validate with IF/ELSEIF
    -- If doctor not found → ERROR
    -- If patient not found → ERROR
    -- If double booking → ERROR with 'DOUBLE BOOKING' message
    -- Else → INSERT and SUCCESS
    IF v_doctor_exists = 0 THEN
        SET p_Status = 'ERROR';
        SET p_Message = 'Doctor not found';
    ELSEIF v_patient_exists = 0 THEN
        SET p_Status = 'ERROR';
        SET p_Message = 'Patient not found';
    ELSEIF v_double_booking > 0 THEN
        SET p_Status = 'ERROR';
        SET p_Message = 'DOUBLE BOOKING: Doctor already has appointment at this time';
    ELSE
        INSERT INTO Appointments (AppointmentID, DoctorID, PatientID, AppointmentDate, AppointmentTime)
        VALUES (p_AppointmentID, p_DoctorID, p_PatientID, p_AppointmentDate, p_AppointmentTime);
        SET p_Status = 'SUCCESS';
        SET p_Message = 'Appointment scheduled successfully';
    END IF;
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
    DECLARE v_patient_exists INT DEFAULT 0;

    -- TODO: Check patient exists
    SELECT COUNT(*) INTO v_patient_exists
    FROM Patients
    WHERE PatientID = (p_PatientID COLLATE utf8mb4_unicode_ci);

    -- TODO: Check amount >= 0
    -- TODO: INSERT INTO Invoices
    -- TODO: SET status and message
    IF v_patient_exists = 0 THEN
        SET p_Status = 'ERROR';
        SET p_Message = 'Patient not found';
    ELSEIF p_TotalAmount < 0 THEN
        SET p_Status = 'ERROR';
        SET p_Message = 'Total amount cannot be negative';
    ELSE
        INSERT INTO Invoices (InvoiceID, PatientID, InvoiceDate, TotalAmount)
        VALUES (p_InvoiceID, p_PatientID, p_InvoiceDate, p_TotalAmount);
        SET p_Status = 'SUCCESS';
        SET p_Message = 'Invoice generated successfully';
    END IF;
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
    DECLARE v_appointment_exists INT DEFAULT 0;

    -- TODO: Check appointment exists
    SELECT COUNT(*) INTO v_appointment_exists
    FROM Appointments
    WHERE AppointmentID = (p_AppointmentID COLLATE utf8mb4_unicode_ci);

    -- TODO: DELETE FROM Appointments
    -- TODO: SET status and message
    IF v_appointment_exists = 0 THEN
        SET p_Status = 'ERROR';
        SET p_Message = 'Appointment not found';
    ELSE
        DELETE FROM Appointments
        WHERE AppointmentID = (p_AppointmentID COLLATE utf8mb4_unicode_ci);
        SET p_Status = 'SUCCESS';
        SET p_Message = 'Appointment cancelled successfully';
    END IF;
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
    SELECT 'Patient Information:' AS Section;
    SELECT PatientID, PatientName, DateOfBirth, Gender, Address, PhoneNumber
    FROM Patients
    WHERE PatientID = (p_PatientID COLLATE utf8mb4_unicode_ci);

    -- TODO: SELECT appointment history (JOIN with Doctors, Departments)
    -- ORDER BY AppointmentDate DESC
    SELECT 'Appointment History:' AS Section;
    SELECT a.AppointmentID, a.AppointmentDate, a.AppointmentTime,
           d.DoctorName, d.Specialty, dept.DepartmentName
    FROM Appointments a
    JOIN Doctors d ON a.DoctorID = d.DoctorID
    JOIN Departments dept ON d.DepartmentID = dept.DepartmentID
    WHERE a.PatientID = (p_PatientID COLLATE utf8mb4_unicode_ci)
    ORDER BY a.AppointmentDate DESC, a.AppointmentTime DESC;

    -- TODO: SELECT invoice history
    -- ORDER BY InvoiceDate DESC
    SELECT 'Invoice History:' AS Section;
    SELECT InvoiceID, InvoiceDate, TotalAmount
    FROM Invoices
    WHERE PatientID = (p_PatientID COLLATE utf8mb4_unicode_ci)
    ORDER BY InvoiceDate DESC;
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
    SELECT 'Daily Summary:' AS Section;
    SELECT 
        COUNT(DISTINCT a.AppointmentID) AS TotalAppointments,
        COUNT(DISTINCT i.InvoiceID) AS TotalInvoices,
        COALESCE(SUM(i.TotalAmount), 0) AS TotalRevenue
    FROM Appointments a
    LEFT JOIN Invoices i ON a.PatientID = i.PatientID AND a.AppointmentDate = i.InvoiceDate
    WHERE a.AppointmentDate = p_ReportDate;

    -- TODO: Appointment details for the date
    SELECT 'Appointment Details:' AS Section;
    SELECT a.AppointmentID, a.AppointmentTime,
           d.DoctorName, d.Specialty,
           p.PatientName, p.PhoneNumber
    FROM Appointments a
    JOIN Doctors d ON a.DoctorID = d.DoctorID
    JOIN Patients p ON a.PatientID = p.PatientID
    WHERE a.AppointmentDate = p_ReportDate
    ORDER BY a.AppointmentTime;

    -- TODO: Invoice details for the date
    SELECT 'Invoice Details:' AS Section;
    SELECT i.InvoiceID, i.TotalAmount,
           p.PatientName
    FROM Invoices i
    JOIN Patients p ON i.PatientID = p.PatientID
    WHERE i.InvoiceDate = p_ReportDate
    ORDER BY i.TotalAmount DESC;
END$$

DELIMITER ;

-- =====================================================
-- VERIFY
-- =====================================================
SHOW PROCEDURE STATUS WHERE Db = 'hospital_db';
