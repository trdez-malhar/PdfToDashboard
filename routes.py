import os
import fitz  # PyMuPDF
from flask import Flask, request, render_template, jsonify, Blueprint
from config import UPLOAD_FOLDER
from utils.file_handler import allowed_file
from utils.pdf_processor import save_and_extract, get_dashboard_data
from db import insert_data, read_predefined_data

# api_routes.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

api_routes = Blueprint("api_routes", __name__)
# Constants

@api_routes.route("/dashboard")
def dashboard():
    # data = get_dashboard_data()
    status = read_predefined_data()
    # status = insert_data_bulk(table_name="cas_users",records=[{"name" : data["client_info"]["name"]}])
    if status:
        return jsonify(status)
    # return jsonify({"status": "error", "message": "Failed to insert data into the database."})
    return jsonify({"status": "error", "message": "Failed to insert data into the database."})

@api_routes.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"status": "error", "message": "No file part"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"status": "error", "message": "No selected file"})

    if file and allowed_file(file.filename):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        try:
            with fitz.open(filepath) as doc:
                if len(doc) == 0:
                    return jsonify({"status": "error", "message": "Empty PDF"})

                first_page_text = doc[0].get_text("text")
                if "consolidated account statement" not in first_page_text.lower():
                    return jsonify({"status": "error", "message": "Invalid document"})

        except Exception as e:
            return jsonify({"status": "error", "message": f"PDF validation failed: {str(e)}"})

        save_and_extract(filepath)
        return jsonify({"status": "success", "message": f"File uploaded successfully: {file.filename}"})

    return jsonify({"status": "error", "message": "Invalid file format. Only PDFs allowed."})
