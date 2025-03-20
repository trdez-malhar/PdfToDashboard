import json
import time
import fitz  # PyMuPDF
import re
import numpy as np
import pandas as pd
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from utils.file_handler import dataframe_to_dict, clean_strings
from config import EXTRACTED_TABLES
from .external_data import get_isin_data, get_company_profile
from datetime import datetime

# Predefined Data Structure
predefined_data = {
    "client_info": {"name": None},
    "accounts": None,
    "portfolio": None,
    "asset_allocation": None,
    "CDSLHoldings": None,
    "MFHoldings": None,
}

# Function to clean NAV column
def clean_nav(value):
    if isinstance(value, str):
        # Remove soft hyphens and unwanted spaces/dashes
        value = value.replace("\xad", "").replace("­", "").replace("-", " ")
        
        # Extract numeric parts
        numbers = re.findall(r'\d+\.\d+|\d+', value)

        if len(numbers) == 2:
            # Case 1: "642.901 306.2378" -> Keep only the second part (306.2378)
            if "." in numbers[1]:  
                return float(numbers[1])
            # Case 2: "1379.4 304" -> Merge correctly into "1379.4304"
            return float(numbers[0] + numbers[1])  
        elif numbers:
            return float(numbers[0])  # If only one valid number, return it
    return value  # Return NaN as is

def extract_pdf_data(source: str):
    """Extract data from a PDF using DocumentConverter."""
    pipeline_options = PdfPipelineOptions(
        do_ocr=True,  
        do_table_structure=True,
        table_detection_mode="lattice",
    )
    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )
    result = converter.convert(source)
    result = result.document.export_to_dict()
    with open(f"extracted_data_{int(time.time())}.json", "w", encoding="utf-8") as fp:
        json.dump(result, fp, indent=4)

    return result

def process_holdings_data(df):
    """Process CDSL and Mutual Fund holdings data."""
    df.replace("", pd.NA, inplace=True)
    if df.columns[0] == "ISINISIN":
        df.dropna(subset=["ISINISIN"], inplace=True)
        cols_to_convert = ["CurrentBal", "FreeBal", "MarketPriceFaceValue", "Value"]
        df[cols_to_convert] = df[cols_to_convert].replace(",", "", regex=True).apply(pd.to_numeric)
        df.dropna(subset=["CurrentBal", "FreeBal", "MarketPriceFaceValue", "Value"], inplace=True)
        df.reset_index(drop=True, inplace=True)
        # isin_list = df["ISINISIN"].tolist()
        # isin_data = [get_isin_data(isin) for isin in isin_list]
        # df["symbol"] = isin_data
        # df["industry"] = [get_company_profile(symbol) for symbol in isin_data]
        rename_col = {"ISINISIN":"isin","Security":"security","CurrentBal":"currentbal"
                      ,"FreeBal":"freebal","MarketPriceFaceValue":"marketpricefacevalue",
                      "Value" : "value"}
        df.rename(columns=rename_col, inplace=True)
        df = df[["isin","security","currentbal","freebal","marketpricefacevalue","value"]]
        predefined_data["CDSLHoldings"] = dataframe_to_dict(df)
    elif df.columns[0] == "SchemeName":
        df.dropna(subset=["SchemeName"], inplace=True)
        df = df[df["SchemeName"] != "Grand Total"]
        df.columns = df.columns.str.lower()
        rename_col = {df.columns[len(df.columns) - 3]: "averagetotalexpenseratio",
                      df.columns[len(df.columns) - 1]: "grosscommissionpaidtodistributors",
                      df.columns[len(df.columns) - 5] : "cumulativeamountinvested"}
        df.rename(columns = rename_col, inplace=True)
        
        df = df[['schemename', 'isin', 'nav',
       'cumulativeamountinvested', 'valuation',
       'averagetotalexpenseratio',
       'grosscommissionpaidtodistributors']]
        print(df.columns)
        df["nav"] = df["nav"].apply(clean_nav)
        cols_to_convert = [ "cumulativeamountinvested", "valuation", 
                           "averagetotalexpenseratio","grosscommissionpaidtodistributors"]
        df[cols_to_convert] = df[cols_to_convert].replace(",", "", regex=True).apply(pd.to_numeric)
        predefined_data["MFHoldings"] = dataframe_to_dict(df)

def process_tables(response):
    """Process extracted tables and update predefined_data."""
    for i, table_data in enumerate(response.get("tables", [])):
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
        df.replace("", pd.NA, inplace=True)
        if i == 0:
            predefined_data["client_info"]["name"] = df["NameJointNames"][0]
        elif i == 1:
            if "Account Type" in df.iloc[0,0]:
               df.columns = df.iloc[0]  # Set new headers
               df = df[1:].reset_index(drop=True)
               print("inside ",df.columns)
               df.columns = clean_strings(df.columns.tolist())
               
            df.columns = clean_strings(df.columns.tolist())
            new_values = ["name", "details", "num_isin_scheme", "value"]
            rename_columns = dict(zip(df.columns, new_values))
            print(rename_columns)
            df.rename(columns=rename_columns, inplace=True)
            print(df)
            df.dropna(subset=["name"], inplace=True)
            df["num_isin_scheme"] = df["num_isin_scheme"].str.replace(",", "").astype(float)
            df["value"] = df["value"].str.replace(",", "").astype(float)
            df.reset_index(drop=True, inplace=True)  
            predefined_data["accounts"] = dataframe_to_dict(df)
        elif i == 2:
            if "Portfolio" in df.columns[1]:
                rename_columns = {df.columns[1] : "PortfolioValuationIn"}
                df.rename(columns=rename_columns, inplace=True)
            df["PortfolioValuationIn"] = df["PortfolioValuationIn"].str.replace(",", "").astype(float)
            df = df[["MonthYear","PortfolioValuationIn"]]
            df.sort_values(by='PortfolioValuationIn', inplace=True, ascending=True)
            df.reset_index(drop=True, inplace=True)  
            df.rename(columns={"PortfolioValuationIn" : "value"}, inplace=True)
                        # Convert MonthYear column to datetime format
            df['MonthYear'] = pd.to_datetime(df['MonthYear'], format="%b %Y")
            # Extract full month name and year
            df['month'] = df['MonthYear'].dt.strftime('%B')  # Full month name (e.g., 'April')
            df['year'] = df['MonthYear'].dt.year  # Extract year
            df = df[["month", "year", "value"]]
            predefined_data["portfolio"] = dataframe_to_dict(df)
        elif i == 3:
            df["Value"] = df["Value"].str.replace(",", "").astype(float)            
            df = df[df['AssetClass'] != 'Total']
            df.rename(columns={"AssetClass" : "name"}, inplace=True)
            predefined_data["asset_allocation"] = dataframe_to_dict(df)
        elif i > 4:
            process_holdings_data(df)

    final_filename = f"final_data_{predefined_data['client_info']['name']}.json"
    with open(final_filename, "w") as json_file:
        json.dump(predefined_data, json_file, indent=4)

def save_and_extract(filepath):
    """Save uploaded PDF and extract tables."""
    response = extract_pdf_data(filepath)
    process_tables(response)
    return predefined_data