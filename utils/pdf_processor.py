import json
import time
import fitz  # PyMuPDF
import pandas as pd
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from utils.file_handler import dataframe_to_dict, clean_strings
from config import EXTRACTED_TABLES

# Predefined Data Structure
predefined_data = {
    "client_info": {"name": None},
    "accounts": None,
    "portfolio": {"month_wise": None},
    "asset_allocation": None,
    "CDSLHoldings": None,
    "MFHoldings": None,
}
def get_dashboard_data():
    return predefined_data
def extract_pdf_data(source: str):
    """Extract data from a PDF using DocumentConverter."""
    pipeline_options = PdfPipelineOptions(
        do_ocr=False,  
        do_table_structure=True,
        table_detection_mode="lattice",
    )
    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )
    result = converter.convert(source)

    with open("extracted_data.json", "w", encoding="utf-8") as fp:
        json.dump(result.document.export_to_dict(), fp, indent=4)

def process_holdings_data(df):
    """Process CDSL and Mutual Fund holdings data."""
    df.replace("", pd.NA, inplace=True)
    if df.columns[0] == "ISINISIN":
        df.dropna(subset=["ISINISIN"], inplace=True)
        predefined_data["CDSLHoldings"] = dataframe_to_dict(df)
    elif df.columns[0] == "SchemeName":
        df.dropna(subset=["SchemeName"], inplace=True)
        df.drop(df[df["SchemeName"] == "Grand Total"].index, inplace=True)
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
            row_idx, col_idx = cell["start_row_offset_idx"], cell["start_col_offset_idx"]
            text = cell["text"]
            if row_idx not in table:
                table[row_idx] = [""] * max_columns
            table[row_idx][col_idx] = text

        structured_data = [table[row] for row in sorted(table.keys())]
        columns = clean_strings(structured_data.pop(0))
        df = pd.DataFrame(structured_data, columns=columns)

        timestamp = int(time.time())
        csv_filename = f"extracted_table_{i+1}_{timestamp}.csv"
        df.to_csv(f"{EXTRACTED_TABLES}/{csv_filename}", index=False)

        if i == 0:
            predefined_data["client_info"]["name"] = df["NameJointNames"][0]
        elif i == 1:
            predefined_data["accounts"] = dataframe_to_dict(df)
        elif i == 2:
            predefined_data["portfolio"]["month_wise"] = dataframe_to_dict(df)
        elif i == 3:
            predefined_data["asset_allocation"] = dataframe_to_dict(df)
        elif i > 4:
            process_holdings_data(df)

    final_filename = f"final_data_{predefined_data['client_info']['name']}.json"
    with open(final_filename, "w") as json_file:
        json.dump(predefined_data, json_file, indent=4)

def save_and_extract(filepath):
    """Save uploaded PDF and extract tables."""
    extract_pdf_data(filepath)
    process_tables()
