-- =====================================================
-- SCRIPT 05: ADVANCED VIEWS
-- Hospital Management System - NEU DATCOM Lab
-- Theo yêu cầu: "Views for frequently accessed queries"
-- =====================================================

USE hospital_db;

-- =====================================================
-- ⭐ VIEW 1: Lịch hẹn hôm nay (Daily Appointments)
-- Purpose: Dashboard / lễ tân tra cứu nhanh
-- TODO: Create a VIEW that shows today's appointments with:
--   - AppointmentID, AppointmentDate, AppointmentTime
--   - DoctorName, Specialty, DepartmentName
--   - PatientName, PhoneNumber
-- HINT: JOIN Appointments with Doctors, Departments, and Patients
-- HINT: WHERE AppointmentDate = CURDATE()
-- HINT: ORDER BY AppointmentTime
-- =====================================================
CREATE OR REPLACE VIEW vw_daily_appointments AS
SELECT 
    a.AppointmentID,
    a.AppointmentDate,
    a.AppointmentTime,
    d.DoctorName,
    d.Specialty,
    dept.DepartmentName,
    p.PatientName,
    p.PhoneNumber
FROM Appointments a
JOIN Doctors d ON a.DoctorID = d.DoctorID
JOIN Departments dept ON d.DepartmentID = dept.DepartmentID
JOIN Patients p ON a.PatientID = p.PatientID
WHERE a.AppointmentDate = CURDATE()
ORDER BY a.AppointmentTime;


-- =====================================================
-- ⭐ VIEW 2: Thống kê doanh thu theo tháng (Monthly Revenue)
-- Purpose: Báo cáo tài chính
-- TODO: Create a VIEW that shows monthly revenue:
--   - Year, Month, YearMonth (formatted)
--   - TotalInvoices (COUNT)
--   - TotalRevenue (SUM), AvgInvoiceAmount (AVG)
--   - MinInvoice, MaxInvoice
-- HINT: GROUP BY YEAR(InvoiceDate), MONTH(InvoiceDate)
-- =====================================================
CREATE OR REPLACE VIEW vw_monthly_revenue AS
SELECT 
    YEAR(InvoiceDate) AS Year,
    MONTH(InvoiceDate) AS Month,
    DATE_FORMAT(InvoiceDate, '%Y-%m') AS YearMonth,
    COUNT(*) AS TotalInvoices,
    SUM(TotalAmount) AS TotalRevenue,
    AVG(TotalAmount) AS AvgInvoiceAmount,
    MIN(TotalAmount) AS MinInvoice,
    MAX(TotalAmount) AS MaxInvoice
FROM Invoices
GROUP BY YEAR(InvoiceDate), MONTH(InvoiceDate), DATE_FORMAT(InvoiceDate, '%Y-%m')
ORDER BY Year DESC, Month DESC;


-- =====================================================
-- ⭐ VIEW 3: Số lượt khám theo bác sĩ (Doctor Performance)
-- Purpose: Đánh giá hiệu suất bác sĩ
-- TODO: Create a VIEW that shows:
--   - DoctorID, DoctorName, Specialty, DepartmentName
--   - TotalAppointments (COUNT)
-- HINT: LEFT JOIN to include doctors with 0 appointments
-- HINT: ORDER BY TotalAppointments DESC
-- =====================================================
CREATE OR REPLACE VIEW vw_doctor_appointments AS
SELECT 
    d.DoctorID,
    d.DoctorName,
    d.Specialty,
    dept.DepartmentName,
    COUNT(a.AppointmentID) AS TotalAppointments
FROM Doctors d
LEFT JOIN Appointments a ON d.DoctorID = a.DoctorID
JOIN Departments dept ON d.DepartmentID = dept.DepartmentID
GROUP BY d.DoctorID, d.DoctorName, d.Specialty, dept.DepartmentName
ORDER BY TotalAppointments DESC;


-- =====================================================
-- ⭐ VIEW 4: Lịch sử khám bệnh nhân (Patient Visit History)
-- Purpose: Báo cáo patient visits (yêu cầu đề bài)
-- TODO: Create a VIEW that shows:
--   - PatientID, PatientName, DateOfBirth, Gender
--   - TotalVisits (COUNT appointments)
--   - FirstVisit, LastVisit (MIN/MAX appointment date)
--   - TotalSpent (SUM invoice amounts)
-- HINT: LEFT JOIN both Appointments and Invoices
-- =====================================================
CREATE OR REPLACE VIEW vw_patient_visit_history AS
SELECT 
    p.PatientID,
    p.PatientName,
    p.DateOfBirth,
    p.Gender,
    COUNT(DISTINCT a.AppointmentID) AS TotalVisits,
    MIN(a.AppointmentDate) AS FirstVisit,
    MAX(a.AppointmentDate) AS LastVisit,
    COALESCE(SUM(i.TotalAmount), 0) AS TotalSpent
FROM Patients p
LEFT JOIN Appointments a ON p.PatientID = a.PatientID
LEFT JOIN Invoices i ON p.PatientID = i.PatientID
GROUP BY p.PatientID, p.PatientName, p.DateOfBirth, p.Gender
ORDER BY TotalVisits DESC;


-- =====================================================
-- ⭐ VIEW 5: Thống kê theo khoa (Department Summary)
-- Purpose: Quản lý phân bổ nguồn lực
-- TODO: Create a VIEW that shows:
--   - DepartmentID, DepartmentName
--   - TotalDoctors, TotalAppointments, TotalRevenue
-- HINT: Multiple LEFT JOINs from Departments → Doctors → Appointments → Invoices
-- =====================================================
CREATE OR REPLACE VIEW vw_department_summary AS
SELECT 
    dept.DepartmentID,
    dept.DepartmentName,
    COUNT(DISTINCT d.DoctorID) AS TotalDoctors,
    COUNT(DISTINCT a.AppointmentID) AS TotalAppointments,
    COALESCE(SUM(i.TotalAmount), 0) AS TotalRevenue
FROM Departments dept
LEFT JOIN Doctors d ON dept.DepartmentID = d.DepartmentID
LEFT JOIN Appointments a ON d.DoctorID = a.DoctorID
LEFT JOIN Invoices i ON a.PatientID = i.PatientID
GROUP BY dept.DepartmentID, dept.DepartmentName
ORDER BY TotalAppointments DESC;


-- =====================================================
-- VERIFY & TEST
-- =====================================================
SHOW FULL TABLES WHERE Table_type = 'VIEW';

-- TODO: Test each view with SELECT * FROM view_name;
-- SELECT * FROM vw_daily_appointments;
-- SELECT * FROM vw_monthly_revenue;
-- SELECT * FROM vw_doctor_appointments;
-- SELECT * FROM vw_patient_visit_history;
-- SELECT * FROM vw_department_summary;
