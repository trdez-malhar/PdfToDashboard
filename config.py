import os

# Constants
UPLOAD_FOLDER = "uploads"
EXTRACTED_TABLES = "data/extracted_tables"
ALLOWED_EXTENSIONS = {"pdf"}

# Ensure required directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACTED_TABLES, exist_ok=True)
