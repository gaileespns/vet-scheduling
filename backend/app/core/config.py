
"""Application configuration from environment variables"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("WARNING: DATABASE_URL is not set.")

# JWT Configuration
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your-super-secret-jwt-key-change-in-production")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.environ.get("JWT_EXPIRE_MINUTES", "1440"))  # 24 hours

# Admin Configuration
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@vetclinic.com")

# CORS
BACKEND_CORS_ORIGINS = os.environ.get("BACKEND_CORS_ORIGINS", "*").split(",")

# Logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

# Environment
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")

# Timezone
CLINIC_TIMEZONE = os.environ.get("CLINIC_TIMEZONE", "Asia/Manila")

# Handle NeonDB specific SSL requirements
connect_args = {}
if DATABASE_URL and "neon.tech" in DATABASE_URL:
    connect_args = {"sslmode": "require"}