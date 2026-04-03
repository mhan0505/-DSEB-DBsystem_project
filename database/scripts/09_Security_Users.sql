-- =====================================================
-- SCRIPT 09: SECURITY & USER MANAGEMENT
-- Hospital Management System - NEU DATCOM Lab
-- Theo yêu cầu: "User roles and permissions"
-- =====================================================

USE hospital_db;

-- =====================================================
-- TODO: Create 5 user roles with appropriate permissions
--
-- ROLE 1: admin_hospital (Full access)
--   - GRANT ALL PRIVILEGES ON hospital_db.* WITH GRANT OPTION
--
-- ROLE 2: doctor_user (Read patients, manage appointments)
--   - SELECT on Patients, Doctors, Departments, Invoices
--   - SELECT, INSERT, UPDATE on Appointments
--   - EXECUTE on sp_schedule_appointment, sp_get_patient_history
--
-- ROLE 3: receptionist (Manage patients & appointments)
--   - SELECT, INSERT, UPDATE on Patients
--   - SELECT, INSERT, UPDATE, DELETE on Appointments
--   - EXECUTE on sp_schedule_appointment, sp_cancel_appointment
--
-- ROLE 4: accountant (Manage invoices & reports)
--   - SELECT on Patients, Appointments
--   - SELECT, INSERT, UPDATE on Invoices
--   - SELECT on financial views
--   - EXECUTE on sp_generate_invoice, sp_daily_report
--
-- ROLE 5: readonly_user (View only - auditing)
--   - SELECT on all tables
-- =====================================================

-- HINT: CREATE USER syntax:
-- CREATE USER IF NOT EXISTS 'username'@'localhost' IDENTIFIED BY 'Password123!';

-- HINT: GRANT syntax:
-- GRANT SELECT, INSERT ON hospital_db.TableName TO 'username'@'localhost';

-- HINT: Don't forget FLUSH PRIVILEGES at the end!

-- TODO: Create admin_hospital user


-- TODO: Create doctor_user


-- TODO: Create receptionist


-- TODO: Create accountant


-- TODO: Create readonly_user


-- TODO: FLUSH PRIVILEGES

-- VERIFY
-- SHOW GRANTS FOR 'admin_hospital'@'localhost';
