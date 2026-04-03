-- =====================================================
-- SCRIPT 07: USER DEFINED FUNCTIONS
-- Hospital Management System - NEU DATCOM Lab
-- Theo yêu cầu: "Custom functions for specialized
--   computations (e.g., billing)"
-- =====================================================

USE hospital_db;

DROP FUNCTION IF EXISTS fn_calculate_invoice_total;
DROP FUNCTION IF EXISTS fn_get_patient_age;
DROP FUNCTION IF EXISTS fn_get_doctor_appointment_count;
DROP FUNCTION IF EXISTS fn_get_patient_total_spent;

DELIMITER $$

-- =====================================================
-- ⭐ FUNCTION 1: Tính tổng tiền hóa đơn
-- Input: PatientID, InvoiceDate
-- Output: DECIMAL(10,2) - total amount
-- Logic: Count appointments for patient on that date × 50,000 VND
--
-- TODO: Implement:
--   1. DECLARE variables for count and fee (50000.00)
--   2. SELECT COUNT(*) from Appointments WHERE patient + date match
--   3. Calculate total = count × fee
--   4. RETURN total
-- =====================================================
CREATE FUNCTION fn_calculate_invoice_total(
    p_PatientID     VARCHAR(10),
    p_InvoiceDate   DATE
)
RETURNS DECIMAL(10, 2)
DETERMINISTIC
READS SQL DATA
BEGIN
    -- TODO: Declare v_appointment_count and v_consultation_fee (50000.00)

    -- TODO: Count appointments for this patient on this date

    -- TODO: Calculate and return total

    RETURN 0.00;
END$$

-- =====================================================
-- FUNCTION 2: Tính tuổi bệnh nhân
-- Input: PatientID
-- Output: INT - age in years
-- TODO: Get DateOfBirth, then use TIMESTAMPDIFF(YEAR, dob, CURDATE())
-- =====================================================
CREATE FUNCTION fn_get_patient_age(
    p_PatientID VARCHAR(10)
)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    -- TODO: Get DateOfBirth from Patients table
    -- TODO: Calculate age using TIMESTAMPDIFF
    -- TODO: Return age

    RETURN 0;
END$$

-- =====================================================
-- FUNCTION 3: Đếm lượt hẹn của bác sĩ trong khoảng thời gian
-- Input: DoctorID, StartDate, EndDate
-- Output: INT - appointment count
-- TODO: COUNT appointments WHERE date BETWEEN start AND end
-- =====================================================
CREATE FUNCTION fn_get_doctor_appointment_count(
    p_DoctorID      VARCHAR(10),
    p_StartDate     DATE,
    p_EndDate       DATE
)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    -- TODO: Count and return appointments for doctor in date range

    RETURN 0;
END$$

-- =====================================================
-- FUNCTION 4: Tổng chi tiêu của bệnh nhân
-- Input: PatientID
-- Output: DECIMAL(10,2) - total spent
-- TODO: SUM(TotalAmount) FROM Invoices WHERE PatientID matches
-- HINT: Use COALESCE to handle NULL (when no invoices)
-- =====================================================
CREATE FUNCTION fn_get_patient_total_spent(
    p_PatientID VARCHAR(10)
)
RETURNS DECIMAL(10, 2)
DETERMINISTIC
READS SQL DATA
BEGIN
    -- TODO: Sum all invoice amounts for this patient
    -- HINT: COALESCE(SUM(TotalAmount), 0)

    RETURN 0.00;
END$$

DELIMITER ;

-- =====================================================
-- TEST YOUR FUNCTIONS
-- =====================================================
-- TODO: Test each function:
-- SELECT fn_calculate_invoice_total('P001', '2024-12-02');
-- SELECT PatientName, fn_get_patient_age(PatientID) AS Age FROM Patients;
-- SELECT DoctorName, fn_get_doctor_appointment_count(DoctorID, '2024-12-01', '2024-12-31') FROM Doctors;
-- SELECT PatientName, fn_get_patient_total_spent(PatientID) FROM Patients;
