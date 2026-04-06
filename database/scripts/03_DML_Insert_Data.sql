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

INSERT INTO Departments (DepartmentID, DepartmentName) VALUES
('DEP001', 'Cardiology'),
('DEP002', 'Neurology'),
('DEP003', 'Orthopedics'),
('DEP004', 'Pediatrics'),
('DEP005', 'Dermatology'),
('DEP006', 'General Medicine');


-- =====================================================
-- 2. PATIENTS (ít nhất 8 bản ghi - dữ liệu thực tế VN)
-- TODO: Insert at least 8 patients with Vietnamese names
-- HINT: ('P001', 'Nguyen Van An', '1985-03-15', 'M', '12 Tran Hung Dao, Ha Noi', '0901234567')
-- =====================================================

INSERT INTO Patients (PatientID, PatientName, DateOfBirth, Gender, Address, PhoneNumber) VALUES
('P001', 'Nguyen Van An', '1985-03-15', 'M', '12 Tran Hung Dao, Ha Noi', '0901234567'),
('P002', 'Tran Thi Binh', '1990-07-22', 'F', '45 Le Loi, Da Nang', '0912345678'),
('P003', 'Le Van Cuong', '1978-11-30', 'M', '78 Nguyen Hue, TP HCM', '0923456789'),
('P004', 'Pham Thi Dung', '1995-02-14', 'F', '23 Hang Bai, Ha Noi', '0934567890'),
('P005', 'Hoang Van Eminh', '1982-09-05', 'M', '56 Vo Van Tan, Can Tho', '0945678901'),
('P006', 'Do Thi Phuong', '1988-12-20', 'F', '89 Bach Dang, Hai Phong', '0956789012'),
('P007', 'Vu Van Giang', '1975-06-18', 'M', '34 Nguyen Trai, Hue', '0967890123'),
('P008', 'Ngo Thi Huong', '2000-04-25', 'F', '67 Ly Thuong Kiet, Nha Trang', '0978901234');


-- =====================================================
-- 3. DOCTORS (ít nhất 6 bản ghi)
-- TODO: Insert at least 6 doctors
-- HINT: Make sure DepartmentID references an existing department!
-- =====================================================

INSERT INTO Doctors (DoctorID, DoctorName, DepartmentID, Specialty) VALUES
('DOC001', 'Dr. Nguyen Thanh Tung', 'DEP001', 'Heart Surgery'),
('DOC002', 'Dr. Tran Minh Quan', 'DEP002', 'Brain Disorders'),
('DOC003', 'Dr. Le Thi Mai', 'DEP003', 'Bone & Joint'),
('DOC004', 'Dr. Pham Van Duc', 'DEP004', 'Child Health'),
('DOC005', 'Dr. Hoang Thi Lan', 'DEP005', 'Skin Diseases'),
('DOC006', 'Dr. Do Van Khôi', 'DEP006', 'Internal Medicine');


-- =====================================================
-- 4. APPOINTMENTS (ít nhất 8 bản ghi)
-- TODO: Insert at least 8 appointments
-- IMPORTANT: Do NOT create 2 appointments for same doctor at same date+time!
--            (UNIQUE INDEX will reject it)
-- HINT: Spread appointments across different doctors, dates, and times
-- =====================================================

INSERT INTO Appointments (AppointmentID, DoctorID, PatientID, AppointmentDate, AppointmentTime) VALUES
('APT001', 'DOC001', 'P001', '2025-04-10', '08:00:00'),
('APT002', 'DOC002', 'P002', '2025-04-10', '09:00:00'),
('APT003', 'DOC003', 'P003', '2025-04-10', '10:00:00'),
('APT004', 'DOC004', 'P004', '2025-04-11', '08:30:00'),
('APT005', 'DOC005', 'P005', '2025-04-11', '09:30:00'),
('APT006', 'DOC006', 'P006', '2025-04-11', '14:00:00'),
('APT007', 'DOC001', 'P007', '2025-04-12', '08:00:00'),
('APT008', 'DOC002', 'P008', '2025-04-12', '10:00:00');


-- =====================================================
-- 5. INVOICES (ít nhất 6 bản ghi)
-- TODO: Insert at least 6 invoices
-- NOTE: If triggers are active, appointments may auto-create invoices.
--       In that case, you may skip manual invoice insertion.
-- =====================================================

INSERT INTO Invoices (InvoiceID, PatientID, InvoiceDate, TotalAmount) VALUES
('INV001', 'P001', '2025-04-10', 1500000.00),
('INV002', 'P002', '2025-04-10', 2300000.00),
('INV003', 'P003', '2025-04-10', 1800000.00),
('INV004', 'P004', '2025-04-11', 950000.00),
('INV005', 'P005', '2025-04-11', 1200000.00),
('INV006', 'P006', '2025-04-11', 3500000.00);


-- =====================================================
-- VERIFY DATA
-- TODO: Write a query to count records in each table
-- HINT: SELECT 'TableName' AS TableName, COUNT(*) FROM TableName UNION ALL ...
-- =====================================================

SELECT 'Departments' AS TableName, COUNT(*) AS RecordCount FROM Departments
UNION ALL
SELECT 'Patients', COUNT(*) FROM Patients
UNION ALL
SELECT 'Doctors', COUNT(*) FROM Doctors
UNION ALL
SELECT 'Appointments', COUNT(*) FROM Appointments
UNION ALL
SELECT 'Invoices', COUNT(*) FROM Invoices;