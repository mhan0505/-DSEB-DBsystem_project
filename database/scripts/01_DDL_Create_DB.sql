-- =====================================================
-- SCRIPT 01: CREATE DATABASE
-- Hospital Management System - NEU DATCOM Lab
-- =====================================================

-- Drop the database if it already exists (for clean setup)
DROP DATABASE IF EXISTS hospital_db;

-- Create a new database called 'hospital_db'
CREATE DATABASE hospital_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Select the database for use
USE hospital_db;

-- Verify the database was created
SHOW DATABASES LIKE 'hospital_db';