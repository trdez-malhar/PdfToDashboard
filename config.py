import os
from sqlalchemy.engine.url import URL

# Constants
UPLOAD_FOLDER = "uploads"
EXTRACTED_TABLES = "data/extracted_tables"
ALLOWED_EXTENSIONS = {"pdf"}

# Ensure required directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACTED_TABLES, exist_ok=True)

DB_CONFIG = {
    "drivername": "mssql+pyodbc",
    "username": "sa",
    "password": "Tr$ez@2@25",
    "host": "INPUN-S-MWUAT",
    "port": "1433",  # Default SQL Server port
    "database": "Testing",
    "query": {"driver": "ODBC Driver 17 for SQL Server", "TrustServerCertificate": "yes"},
}

DB_URL = URL.create(**DB_CONFIG)
