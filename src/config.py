"""
Configuration module for Hospital Management System.
Database connection settings and application constants.

Mỗi thành viên tạo file .env ở thư mục gốc (copy từ .env.example):
    DB_HOST=localhost
    DB_PORT=3306
    DB_USER=root
    DB_PASSWORD=your_password_here
    DB_NAME=hospital_db

File .env đã được thêm vào .gitignore — KHÔNG commit lên Git.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# =====================================================
# DATABASE CONNECTION SETTINGS (đọc từ .env)
# =====================================================
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'hospital_db'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': False,
    'raise_on_warnings': True
}

# =====================================================
# APPLICATION CONSTANTS
# =====================================================
APP_NAME = "Hospital Management System"
APP_VERSION = "1.0.0"

# TODO: Set the consultation fee (in VND)
CONSULTATION_FEE = 50000.00

# Date/Time formats
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# ID Prefixes
PATIENT_ID_PREFIX = "P"
DOCTOR_ID_PREFIX = "DR"
DEPARTMENT_ID_PREFIX = "D"
APPOINTMENT_ID_PREFIX = "A"
INVOICE_ID_PREFIX = "INV"
