-- =====================================================
-- SCRIPT 04: ADVANCED INDEXES
-- Hospital Management System - NEU DATCOM Lab
-- Tối ưu hiệu năng truy vấn thường dùng
-- =====================================================

USE hospital_db;

-- NOTE: idx_doctor_datetime (UNIQUE) đã tạo trong 02_DDL
-- Các index dưới đây bổ sung cho performance

-- =====================================================
-- PATIENTS INDEXES
-- =====================================================

-- TODO: Create index on PatientName (for search by name)
-- HINT: CREATE INDEX idx_patient_name ON Patients(PatientName);


-- TODO: Create index on PhoneNumber (for quick lookup)


-- =====================================================
-- DOCTORS INDEXES
-- =====================================================

-- TODO: Create index on DepartmentID (for finding doctors by department)


-- TODO: Create index on Specialty (for filtering by specialty)


-- =====================================================
-- APPOINTMENTS INDEXES
-- =====================================================

-- TODO: Create index on AppointmentDate (for daily appointment queries)


-- TODO: Create index on PatientID (for patient appointment history)


-- TODO: Create composite index on (AppointmentDate, AppointmentTime)
-- HINT: Composite indexes optimize queries that filter by both columns


-- =====================================================
-- INVOICES INDEXES
-- =====================================================

-- TODO: Create index on InvoiceDate (for revenue reports)


-- TODO: Create index on PatientID (for patient invoice history)


-- =====================================================
-- VERIFY: Show all indexes
-- TODO: Write a query to list all indexes in the database
-- HINT: Use INFORMATION_SCHEMA.STATISTICS
-- =====================================================
