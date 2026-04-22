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

-- =====================================================
-- DROP EXISTING USERS (for clean re-run)
-- =====================================================
-- DROP USER IF EXISTS 'admin_hospital'@'localhost';
-- DROP USER IF EXISTS 'doctor_user'@'localhost';
-- DROP USER IF EXISTS 'receptionist'@'localhost';
-- DROP USER IF EXISTS 'accountant'@'localhost';
-- DROP USER IF EXISTS 'readonly_user'@'localhost';

-- =====================================================
-- TODO: Create admin_hospital user (Full access)
-- =====================================================
CREATE USER IF NOT EXISTS 'admin_hospital'@'localhost'
    IDENTIFIED BY 'Admin@Hospital2024!';

GRANT ALL PRIVILEGES ON hospital_db.* TO 'admin_hospital'@'localhost'
    WITH GRANT OPTION;

-- =====================================================
-- TODO: Create doctor_user (Read patients, manage appointments)
-- =====================================================
CREATE USER IF NOT EXISTS 'doctor_user'@'localhost'
    IDENTIFIED BY 'Doctor@Hospital2024!';

GRANT SELECT ON hospital_db.Patients TO 'doctor_user'@'localhost';
GRANT SELECT ON hospital_db.Doctors TO 'doctor_user'@'localhost';
GRANT SELECT ON hospital_db.Departments TO 'doctor_user'@'localhost';
GRANT SELECT, INSERT, UPDATE ON hospital_db.Appointments TO 'doctor_user'@'localhost';
GRANT SELECT ON hospital_db.Invoices TO 'doctor_user'@'localhost';
GRANT SELECT ON hospital_db.vw_daily_appointments TO 'doctor_user'@'localhost';
GRANT SELECT ON hospital_db.vw_doctor_appointments TO 'doctor_user'@'localhost';
GRANT SELECT ON hospital_db.vw_patient_visit_history TO 'doctor_user'@'localhost';
GRANT EXECUTE ON PROCEDURE hospital_db.sp_schedule_appointment TO 'doctor_user'@'localhost';
GRANT EXECUTE ON PROCEDURE hospital_db.sp_get_patient_history TO 'doctor_user'@'localhost';

-- =====================================================
-- TODO: Create receptionist (Manage patients & appointments)
-- =====================================================
CREATE USER IF NOT EXISTS 'receptionist'@'localhost'
    IDENTIFIED BY 'Reception@Hospital2024!';

GRANT SELECT, INSERT, UPDATE ON hospital_db.Patients TO 'receptionist'@'localhost';
GRANT SELECT ON hospital_db.Doctors TO 'receptionist'@'localhost';
GRANT SELECT ON hospital_db.Departments TO 'receptionist'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON hospital_db.Appointments TO 'receptionist'@'localhost';
GRANT SELECT ON hospital_db.Invoices TO 'receptionist'@'localhost';
GRANT SELECT ON hospital_db.vw_daily_appointments TO 'receptionist'@'localhost';
GRANT SELECT ON hospital_db.vw_doctor_appointments TO 'receptionist'@'localhost';
GRANT EXECUTE ON PROCEDURE hospital_db.sp_schedule_appointment TO 'receptionist'@'localhost';
GRANT EXECUTE ON PROCEDURE hospital_db.sp_cancel_appointment TO 'receptionist'@'localhost';
GRANT EXECUTE ON PROCEDURE hospital_db.sp_get_patient_history TO 'receptionist'@'localhost';

-- =====================================================
-- TODO: Create accountant (Manage invoices & financial reports)
-- =====================================================
CREATE USER IF NOT EXISTS 'accountant'@'localhost'
    IDENTIFIED BY 'Account@Hospital2024!';

GRANT SELECT ON hospital_db.Patients TO 'accountant'@'localhost';
GRANT SELECT ON hospital_db.Appointments TO 'accountant'@'localhost';
GRANT SELECT, INSERT, UPDATE ON hospital_db.Invoices TO 'accountant'@'localhost';
GRANT SELECT ON hospital_db.vw_monthly_revenue TO 'accountant'@'localhost';
GRANT SELECT ON hospital_db.vw_patient_visit_history TO 'accountant'@'localhost';
GRANT SELECT ON hospital_db.vw_department_summary TO 'accountant'@'localhost';
GRANT EXECUTE ON PROCEDURE hospital_db.sp_generate_invoice TO 'accountant'@'localhost';
GRANT EXECUTE ON PROCEDURE hospital_db.sp_daily_report TO 'accountant'@'localhost';

-- =====================================================
-- TODO: Create readonly_user (View only - auditing)
-- =====================================================
CREATE USER IF NOT EXISTS 'readonly_user'@'localhost'
    IDENTIFIED BY 'ReadOnly@Hospital2024!';

GRANT SELECT ON hospital_db.* TO 'readonly_user'@'localhost';

-- =====================================================
-- TODO: FLUSH PRIVILEGES
-- =====================================================
FLUSH PRIVILEGES;

-- VERIFY
SELECT User, Host FROM mysql.user
WHERE User IN ('admin_hospital', 'doctor_user', 'receptionist', 'accountant', 'readonly_user');

SHOW GRANTS FOR 'admin_hospital'@'localhost';
SHOW GRANTS FOR 'doctor_user'@'localhost';
SHOW GRANTS FOR 'receptionist'@'localhost';
SHOW GRANTS FOR 'accountant'@'localhost';
SHOW GRANTS FOR 'readonly_user'@'localhost';

-- =====================================================
-- BACKUP & RECOVERY NOTES
-- =====================================================
-- Full backup (run from terminal):
--   mysqldump -u admin_hospital -p --routines --triggers hospital_db > hospital_backup.sql
--
-- Restore:
--   mysql -u admin_hospital -p hospital_db < hospital_backup.sql

SELECT 'Security users and permissions configured successfully!' AS Status;
