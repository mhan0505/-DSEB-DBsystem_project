-- =====================================================
-- SCRIPT 02: CREATE TABLES - BUSINESS LOGIC FIRST
-- Hospital Management System - NEU DATCOM Lab
-- 5 bảng theo đúng yêu cầu đề bài
-- =====================================================

USE hospital_db;

-- =====================================================
-- Drop tables in reverse dependency order (for re-run)
-- =====================================================
DROP TABLE IF EXISTS Appointments;
DROP TABLE IF EXISTS Invoices;
DROP TABLE IF EXISTS Doctors;
DROP TABLE IF EXISTS Patients;
DROP TABLE IF EXISTS Departments;

-- =====================================================
-- 1. DEPARTMENTS (Không phụ thuộc bảng nào)
-- TODO: Create table Departments with:
--   - DepartmentID: VARCHAR(10), Primary Key
--   - DepartmentName: VARCHAR(50), NOT NULL, UNIQUE
-- HINT: Use ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
-- =====================================================
CREATE TABLE Departments (
    DepartmentID VARCHAR(10) PRIMARY KEY,
    DepartmentName VARCHAR(50) NOT NULL UNIQUE
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 2. PATIENTS (Không phụ thuộc bảng nào)
-- TODO: Create table Patients with:
--   - PatientID: VARCHAR(10), Primary Key
--   - PatientName: VARCHAR(100), NOT NULL
--   - DateOfBirth: DATE, NOT NULL
--   - Gender: VARCHAR(1), CHECK only allows 'M', 'F', 'O'
--   - Address: VARCHAR(255)
--   - PhoneNumber: VARCHAR(15)
-- =====================================================
CREATE TABLE Patients (
    PatientID VARCHAR(10) PRIMARY KEY,
    PatientName VARCHAR(100) NOT NULL,
    DateOfBirth DATE NOT NULL,
    Gender VARCHAR(1) CHECK (Gender IN ('M', 'F', 'O')),
    Address VARCHAR(255),
    PhoneNumber VARCHAR(15)  
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- =====================================================
-- 3. DOCTORS (Phụ thuộc Departments)
-- TODO: Create table Doctors with:
--   - DoctorID: VARCHAR(10), Primary Key
--   - DoctorName: VARCHAR(100), NOT NULL
--   - DepartmentID: VARCHAR(10), NOT NULL, Foreign Key → Departments
--   - Specialty: VARCHAR(50)
-- HINT: FOREIGN KEY ... ON UPDATE CASCADE ON DELETE RESTRICT
-- =====================================================
CREATE TABLE Doctors (
    DoctorID VARCHAR(10) PRIMARY KEY,
    DoctorName VARCHAR(100) NOT NULL,
    DepartmentID VARCHAR(10) NOT NULL,
    Specialty VARCHAR(50),
    CONSTRAINT fk_doctors_departments
        FOREIGN KEY (DepartmentID)
        REFERENCES Departments(DepartmentID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4;


-- =====================================================
-- 4. INVOICES (Phụ thuộc Patients)
-- TODO: Create table Invoices with:
--   - InvoiceID: VARCHAR(10), Primary Key
--   - PatientID: VARCHAR(10), NOT NULL, Foreign Key → Patients
--   - InvoiceDate: DATE, NOT NULL
--   - TotalAmount: DECIMAL(10,2), NOT NULL, DEFAULT 0.00
-- =====================================================
CREATE TABLE Invoices (
    InvoiceID VARCHAR(10) PRIMARY KEY,
    PatientID VARCHAR(10) NOT NULL,
    InvoiceDate DATE NOT NULL,
    TotalAmount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    CONSTRAINT fk_invoices_patients
        FOREIGN KEY (PatientID)
        REFERENCES Patients(PatientID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- 5. APPOINTMENTS (Phụ thuộc Doctors + Patients)
-- TODO: Create table Appointments with:
--   - AppointmentID: VARCHAR(10), Primary Key
--   - DoctorID: VARCHAR(10), NOT NULL, FK → Doctors
--   - PatientID: VARCHAR(10), NOT NULL, FK → Patients
--   - AppointmentDate: DATE, NOT NULL
--   - AppointmentTime: TIME, NOT NULL
--
-- ⭐ CRITICAL: Add UNIQUE INDEX to prevent double booking!
--   UNIQUE INDEX idx_doctor_datetime (DoctorID, AppointmentDate, AppointmentTime)
--   This ensures 1 doctor cannot have 2 patients at the same date/time
-- =====================================================
CREATE TABLE Appointments (
    AppointmentID VARCHAR(10) PRIMARY KEY,
    DoctorID VARCHAR(10) NOT NULL,
    PatientID VARCHAR(10) NOT NULL,
    AppointmentDate DATE NOT NULL,
    AppointmentTime TIME NOT NULL,
    CONSTRAINT fk_appointments_doctors
        FOREIGN KEY (DoctorID)
        REFERENCES Doctors(DoctorID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_appointments_patients
        FOREIGN KEY (PatientID)
        REFERENCES Patients(PatientID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    UNIQUE INDEX idx_doctor_datetime (DoctorID, AppointmentDate, AppointmentTime)
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================
-- VERIFY TABLE CREATION
-- =====================================================
SHOW TABLES;
