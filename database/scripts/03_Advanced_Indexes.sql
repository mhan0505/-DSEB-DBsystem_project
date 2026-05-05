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
CREATE INDEX idx_patient_name ON Patients(PatientName);

-- TODO: Create index on PhoneNumber (for quick lookup)
CREATE INDEX idx_patient_phone ON Patients(PhoneNumber);


-- =====================================================
-- DOCTORS INDEXES
-- =====================================================

-- TODO: Create index on DepartmentID (for finding doctors by department)
CREATE INDEX idx_doctor_department ON Doctors(DepartmentID);

-- TODO: Create index on Specialty (for filtering by specialty)
CREATE INDEX idx_doctor_specialty ON Doctors(Specialty);


-- =====================================================
-- APPOINTMENTS INDEXES
-- =====================================================

-- TODO: Create index on AppointmentDate (for daily appointment queries)
CREATE INDEX idx_appointment_date ON Appointments(AppointmentDate);

-- TODO: Create index on PatientID (for patient appointment history)
CREATE INDEX idx_appointment_patient ON Appointments(PatientID);

-- TODO: Create composite index on (AppointmentDate, AppointmentTime)
-- HINT: Composite indexes optimize queries that filter by both columns
CREATE INDEX idx_appointment_datetime ON Appointments(AppointmentDate, AppointmentTime);


-- =====================================================
-- INVOICES INDEXES
-- =====================================================

-- TODO: Create index on InvoiceDate (for revenue reports)
CREATE INDEX idx_invoice_date ON Invoices(InvoiceDate);

-- TODO: Create index on PatientID (for patient invoice history)
CREATE INDEX idx_invoice_patient ON Invoices(PatientID);


-- =====================================================
-- VERIFY: Show all indexes
-- TODO: Write a query to list all indexes in the database
-- HINT: Use INFORMATION_SCHEMA.STATISTICS
-- =====================================================
SELECT 
    TABLE_NAME,
    INDEX_NAME,
    COLUMN_NAME,
    SEQ_IN_INDEX,
    NON_UNIQUE
FROM INFORMATION_SCHEMA.STATISTICS 
WHERE TABLE_SCHEMA = 'hospital_db' 
ORDER BY TABLE_NAME, SEQ_IN_INDEX;
