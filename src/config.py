"""
Configuration module for Hospital Management System.
Database connection settings and application constants.

TODO: Fill in the database connection settings for YOUR MySQL setup.
"""

# =====================================================
# DATABASE CONNECTION SETTINGS
# TODO: Update these values to match your MySQL configuration
# =====================================================
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',          # TODO: Enter your MySQL password here
    'database': 'hospital_db',
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
