import unicodedata
import re
import os
import pdfplumber
import csv
# Extract Tables from PDF
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

def savetable(filepath, outputpath):
    # Define the path to the PDF file
    pdf_path = filepath
    # Define the output directory for CSV files
    output_dir = outputpath

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open the PDF
    with pdfplumber.open(pdf_path) as pdf:
        # Iterate through each page in the PDF
        for page_num, page in enumerate(pdf.pages, start=1):
            # Extract tables from the page
            tables = page.extract_tables()
            
            if tables:
                print(f"Tables found on page {page_num}")
                
                for table_index, table in enumerate(tables, start=1):
                    csv_filename = os.path.join(output_dir, f"page_{page_num}_table_{table_index}.csv")
                    
                    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
                        writer = csv.writer(csv_file)
                        for row in table:
                            # Apply text cleaning to each cell
                            cleaned_row = [clean_text(cell) if isinstance(cell, str) else cell for cell in row]
                            
                            writer.writerow(cleaned_row)
                    
                    print(f"Saved cleaned table: {csv_filename}")
            else:
                print(f"No tables found on page {page_num}") 

