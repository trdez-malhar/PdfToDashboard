import os
import fitz  # PyMuPDF
from flask import request, render_template, jsonify, Blueprint, Response, session
from config import UPLOAD_FOLDER
from utils.file_handler import allowed_file
from utils.pdf_processor import save_and_extract
from db import add_data, get_dashboard_data

# api_routes.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

api_routes = Blueprint("api_routes", __name__)
# Constants

@api_routes.route("/dashboard/<int:user_id>")
def dashboard(user_id):
    if user_id:
        print(user_id)
        data = get_dashboard_data(user_id)
        if data:
            return Response(data, content_type="application/json")
    return jsonify(None)

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

        predefined_data = save_and_extract(filepath)
        user_id = add_data(predefined_data)
        if user_id:
            print(user_id)
            session["user_id"] = user_id  # Save user_id in session
            print(session["user_id"])
            return jsonify({
                "status": "success",
                "message": f"File uploaded successfully: {file.filename}",
                "session_id": user_id
            })
    return jsonify({"status": "error", "message": "Invalid file format. Only PDFs allowed."})
