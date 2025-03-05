import unicodedata
import re
import os
import pdfplumber
import csv
import json
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
import pandas as pd
from IPython.display import display
import re
import unicodedata
import json

predefined_data = {
    "accounts" : None,
    "portfolio" : {"month_wise" : None},
    "asset_allocation" : None,
}

html_data_path = ""

def dataframe_to_dict(df):
    # Extract the first column name (it will be dictionary keys)
    dict_key_column = df.columns[0]

    # Drop rows where the first column is NaN (optional, if needed)
    df = df.dropna(subset=[dict_key_column])

    # Convert the DataFrame into a nested dictionary
    result_dict = {}
    for _, row in df.iterrows():
        key = row[dict_key_column]  # First column as the key
        result_dict[key] = row.drop(dict_key_column).to_dict()  # Remaining columns as key-value pairs
    
    return result_dict

def clean_strings(strings):
    return [re.sub(r"[^a-zA-Z]", "", s) for s in strings]

def clean_text(text):
    """Remove non-English characters and normalize text."""
    if text is None:
        return ""
    
    # Normalize Unicode characters
    text = unicodedata.normalize('NFKD', text)
    
    # Remove non-English characters (keep letters, numbers, spaces, and basic punctuation)
    text = re.sub(r'[^A-Za-z0-9\s.,!?;:\'\"()-]', '', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
table_dict = dict()
# Function to extract and display tables
def get_tables(json_data,i):
    raw_data = json_data["tables"][i]["data"]["table_cells"]

    # Determine the max number of columns
    max_columns = max(item["start_col_offset_idx"] + item["col_span"] for item in raw_data)

    # Create an empty table structure
    table = {}

    # Populate table based on extracted data
    for item in raw_data:
        row_idx = item["start_row_offset_idx"]
        col_idx = item["start_col_offset_idx"]
        col_span = item["col_span"]
        text = item["text"]

        # Initialize row if not exists
        if row_idx not in table:
            table[row_idx] = [""] * max_columns  # Initialize empty columns

        # Assign text to correct position, spanning columns if needed
        for j in range(col_span):
            table[row_idx][col_idx + j] = text if j == 0 else ""  # Leave merged columns empty after first

    # Convert table dictionary to a structured list for DataFrame
    structured_data = [table[row] for row in sorted(table.keys())]

    # Extract column headers separately
    columns = structured_data.pop(0)
    columns = clean_strings(columns)
    # Create DataFrame
    df = pd.DataFrame(structured_data, columns=columns)

    # # Display DataFrame using IPython display
    # print(f"\n**Table {i+1}**")

    # display(df)

    if i == 1:
        predefined_data["accounts"] = dataframe_to_dict(df)
        # print(predefined_data)
    if i == 2:
        predefined_data["portfolio"]["month_wise"] = dataframe_to_dict(df)
        # print(predefined_data)
    if i == 3:
        predefined_data["asset_allocation"] = dataframe_to_dict(df)
        # print(predefined_data)


    df.to_csv(f"table_{i+1}.csv", index=False)
    table_dict[f"table_{i+1}"] = df

# source = r"C:\Users\malhar.yadav\Downloads\SEP2024_AA12920184_HLD.PDF"  # document per local path or URL
def extract_pdf_data(source:str, outputpath, file_name) -> None:
        # Set pipeline options to optimize performance
    pipeline_options = PdfPipelineOptions(
        do_ocr=False,  # Disable OCR if the document is digitally generated
        do_table_structure=True,
        table_detection_mode="lattice",
    )

    # Initialize the DocumentConverter with the specified pipeline options
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )
    converter = DocumentConverter()
    result = converter.convert(source)
    # print(result.document.export_to_dict)  # output: "## Docling Technical Report[...]"
    
    with open("weddata.json",mode="w", encoding="utf-8") as fp:
            fp.write(json.dumps(result.document.export_to_dict()))

def savetable(filepath, outputpath, file_name):
    # Define the path to the PDF file
    pdf_path = filepath
    # Define the output directory for CSV files
    output_dir = outputpath

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    extract_pdf_data(pdf_path, output_dir, file_name)
    print("Data extracted successfully.")

def return_data():
    # Loop through tables and display each one
    with open("weddata.json", mode="r", encoding="utf-8") as fp:
        json_data = json.load(fp)

    for i in range(json_data["tables"].__len__()):
        get_tables(json_data, i)
    with open("weddata123.json", "w") as json_file:
            json.dump(predefined_data, json_file, indent=4)  # indent=4 makes it readable
    return predefined_data