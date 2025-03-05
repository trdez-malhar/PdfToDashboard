import os
import re
import json
import time  # Import time module for timestamp generation
# import csv
import unicodedata
import pandas as pd
# import pdfplumber
from flask import Flask, request, render_template, jsonify
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat

# Constants
UPLOAD_FOLDER = "uploads"
EXTRACTED_TABLES = "data/extracted_tables"
ALLOWED_EXTENSIONS = {"pdf"}

# Ensure required directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACTED_TABLES, exist_ok=True)

# Initialize Flask App
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["EXTRACTED_TABLES"] = EXTRACTED_TABLES

# Predefined Data Structure
predefined_data = {
    "accounts": None,
    "portfolio": {"month_wise": None},
    "asset_allocation": None,
    "CDSLHoldings" : None,
    "MFHoldings" : None,
}
def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def dataframe_to_dict(df):
    """Convert a DataFrame to a nested dictionary."""
    dict_key_column = df.columns[0]
    df = df.dropna(subset=[dict_key_column])
    return {row[dict_key_column]: row.drop(dict_key_column).to_dict() for _, row in df.iterrows()}

def clean_strings(strings):
    """Clean column names by removing non-alphabetic characters."""
    return [re.sub(r"[^a-zA-Z]", "", s) for s in strings]

def clean_text(text):
    """Normalize and clean text."""
    if text is None:
        return ""
    text = unicodedata.normalize('NFKD', text)
    text = re.sub(r'[^A-Za-z0-9\s.,!?;:\'"()-]', '', text)
    return re.sub(r'\s+', ' ', text).strip()

def extract_pdf_data(source: str):
    """Extract data from a PDF using DocumentConverter."""
    pipeline_options = PdfPipelineOptions(
        do_ocr=False,  # Assume digitally generated document
        do_table_structure=True,
        table_detection_mode="lattice",
    )
    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )
    result = converter.convert(source)
    
    with open("extracted_data.json", "w", encoding="utf-8") as fp:
        json.dump(result.document.export_to_dict(), fp, indent=4)

def get_same_tables(dfs):
    """Group DataFrames with the same column structure and return lists of matching DataFrames."""
    column_groups = {}

    for df in dfs:
        col_tuple = tuple(df.columns)  # Convert columns to a tuple for hashing
        column_groups.setdefault(col_tuple, []).append(df)

    # Return only groups that contain more than one DataFrame
    return [group for group in column_groups.values() if len(group) > 1]

def process_holdings_data(df):
    print("inside process_holdings_data")
    if df.columns[0] == "ISINISIN":
        if predefined_data["CDSLHoldings"]:
            predefined_data["CDSLHoldings"].update(dataframe_to_dict(df))
        else:
            predefined_data["CDSLHoldings"] = dataframe_to_dict(df)
    elif df.columns[0] == "SchemeName":
        if predefined_data["MFHoldings"]:
            predefined_data["MFHoldings"].update(dataframe_to_dict(df))
        else:
            predefined_data["MFHoldings"] = dataframe_to_dict(df)


def process_tables():
    """Process extracted tables and update predefined_data."""
    with open("extracted_data.json", "r", encoding="utf-8") as fp:
        json_data = json.load(fp)
    
    for i, table_data in enumerate(json_data.get("tables", [])):
        raw_data = table_data["data"]["table_cells"]
        max_columns = max(cell["start_col_offset_idx"] + cell["col_span"] for cell in raw_data)
        
        table = {}
        for cell in raw_data:
            row_idx = cell["start_row_offset_idx"]
            col_idx = cell["start_col_offset_idx"]
            text = cell["text"]
            if row_idx not in table:
                table[row_idx] = [""] * max_columns
            table[row_idx][col_idx] = text
        
        structured_data = [table[row] for row in sorted(table.keys())]
        columns = clean_strings(structured_data.pop(0))
        df = pd.DataFrame(structured_data, columns=columns)
        # Generate a unique filename using a timestamp
        timestamp = int(time.time())  # Get current time in seconds
        csv_filename = f"extracted_table_{i+1}_{timestamp}.csv"
        # csv_filepath = os.path.join(EXTRACTED_TABLES, csv_filename)  # Save in extracted tables folder
        
        # Save DataFrame as CSV
        df.to_csv(csv_filename, index=False)
        if i == 1:
            predefined_data["accounts"] = dataframe_to_dict(df)
        elif i == 2:
            predefined_data["portfolio"]["month_wise"] = dataframe_to_dict(df)
        elif i == 3:
            predefined_data["asset_allocation"] = dataframe_to_dict(df)
        elif i > 4:
            process_holdings_data(df)
            
        
    with open("final_data.json", "w") as json_file:
        json.dump(predefined_data, json_file, indent=4)

def save_and_extract(filepath):
    """Save uploaded PDF and extract tables."""
    extract_pdf_data(filepath)
    process_tables()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", data=predefined_data)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"status": "error", "message": "No file part"})
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"status": "error", "message": "No selected file"})
    
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        save_and_extract(filepath)
        return jsonify({"status": "success", "message": f"File uploaded successfully: {file.filename}"})
    
    return jsonify({"status": "error", "message": "Invalid file format. Only PDFs allowed."})

if __name__ == "__main__":
    app.run(debug=True)
