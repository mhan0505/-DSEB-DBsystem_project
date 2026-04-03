-- =====================================================
-- SCRIPT 03: INSERT SAMPLE DATA
-- Hospital Management System - NEU DATCOM Lab
-- Mỗi bảng cần 5-10 bản ghi thực tế (theo yêu cầu đề bài)
-- =====================================================

USE hospital_db;

-- =====================================================
-- 1. DEPARTMENTS (ít nhất 5 bản ghi)
-- TODO: Insert at least 5 departments
-- HINT: INSERT INTO Departments (DepartmentID, DepartmentName) VALUES ...
-- Suggested: Cardiology, Neurology, Orthopedics, Pediatrics, Dermatology, General Medicine
-- =====================================================


-- =====================================================
-- 2. PATIENTS (ít nhất 8 bản ghi - dữ liệu thực tế VN)
-- TODO: Insert at least 8 patients with Vietnamese names
-- HINT: ('P001', 'Nguyen Van An', '1985-03-15', 'M', '12 Tran Hung Dao, Ha Noi', '0901234567')
-- =====================================================


-- =====================================================
-- 3. DOCTORS (ít nhất 6 bản ghi)
-- TODO: Insert at least 6 doctors
-- HINT: Make sure DepartmentID references an existing department!
-- =====================================================


-- =====================================================
-- 4. APPOINTMENTS (ít nhất 8 bản ghi)
-- TODO: Insert at least 8 appointments
-- IMPORTANT: Do NOT create 2 appointments for same doctor at same date+time!
--            (UNIQUE INDEX will reject it)
-- HINT: Spread appointments across different doctors, dates, and times
-- =====================================================


-- =====================================================
-- 5. INVOICES (ít nhất 6 bản ghi)
-- TODO: Insert at least 6 invoices
-- NOTE: If triggers are active, appointments may auto-create invoices.
--       In that case, you may skip manual invoice insertion.
-- =====================================================


-- =====================================================
-- VERIFY DATA
-- TODO: Write a query to count records in each table
-- HINT: SELECT 'TableName' AS TableName, COUNT(*) FROM TableName UNION ALL ...
-- =====================================================
