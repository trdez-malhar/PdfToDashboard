import json
import time
import pandas as pd
import re
from pathlib import Path
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat

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
    result = result.document.export_to_dict()
    TIMESTAMP = int(time.time())
    PDFOUTPUFILE = F"{OUTPUT_PDF_FOLDER}extracted_data_{TIMESTAMP}.json"
    TABLEOUTPUFILE = F"{OUTPUT_TBALE_FOLDER}extracted_data_{TIMESTAMP}.json"
    with open(PDFOUTPUFILE, "w", encoding="utf-8") as fp:
        json.dump(result, fp, indent=4)
    tables_data = result["tables"]
    with open(TABLEOUTPUFILE, "w", encoding="utf-8") as fp:
        json.dump(tables_data, fp, indent=4)
    return tables_data