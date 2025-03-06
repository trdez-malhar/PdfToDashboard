# import json
# import fitz  # PyMuPDF
# import time
# from docling.datamodel.pipeline_options import PdfPipelineOptions
# from docling.document_converter import DocumentConverter, PdfFormatOption
# from docling.datamodel.base_models import InputFormat
# from concurrent.futures import ProcessPoolExecutor

# PDF_PATH = r"C:\Users\malhar.yadav\scripts\PdfToDashboard\uploads\sb.pdf"

# def extract_page(page_number):
#     """Extract a single page as a new PDF file."""
#     with fitz.open(PDF_PATH) as doc:
#         single_page_pdf = fitz.open()  # Create an empty PDF
#         single_page_pdf.insert_pdf(doc, from_page=page_number, to_page=page_number)
        
#         temp_pdf_path = f"temp_page_{page_number}.pdf"
#         single_page_pdf.save(temp_pdf_path)
#         single_page_pdf.close()
    
#     return temp_pdf_path

# def process_page(page_pdf_path):
#     """Process a single page PDF and return extracted data."""
#     pipeline_options = PdfPipelineOptions(
#         do_ocr=False,  # Assume digitally generated document
#         do_table_structure=True,
#         table_detection_mode="lattice",
#     )
#     converter = DocumentConverter(
#         format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
#     )
    
#     result = converter.convert(page_pdf_path)
#     return result.document.export_to_dict()

# def extract_pdf_data():
#     """Extract and process PDF data with multiprocessing while tracking time."""
    
#     start_time = time.time()  # Start timer
    
#     with fitz.open(PDF_PATH) as doc:
#         num_pages = len(doc)

#     print(f"PDF has {num_pages} pages.")

#     # Step 1: Extract each page as a separate PDF
#     extract_start = time.time()
#     page_pdfs = [extract_page(page_number) for page_number in range(num_pages)]
#     extract_end = time.time()
#     print(f"Page extraction time: {extract_end - extract_start:.2f} seconds")

#     # Step 2: Process each page in parallel
#     process_start = time.time()
#     with ProcessPoolExecutor() as executor:
#         results = list(executor.map(process_page, page_pdfs))
#     process_end = time.time()
#     print(f"Parallel processing time: {process_end - process_start:.2f} seconds")

#     # Step 3: Combine results
#     combine_start = time.time()
#     combined_result = {"tables": []}
#     for result in results:
#         combined_result["tables"].extend(result["tables"])
#     combine_end = time.time()
#     print(f"Data combination time: {combine_end - combine_start:.2f} seconds")

#     # Step 4: Save to JSON
#     save_start = time.time()
#     with open("extracted_data.json", "w", encoding="utf-8") as fp:
#         json.dump(combined_result, fp, indent=4)
#     save_end = time.time()
#     print(f"JSON save time: {save_end - save_start:.2f} seconds")

#     total_time = time.time() - start_time
#     print(f"Total execution time: {total_time:.2f} seconds")
# if __name__ == "__main__":
#     extract_pdf_data()

