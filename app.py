from flask import Flask, request, render_template, jsonify
import os
from data_extractor import savetable
from itertools import zip_longest
import pandas as pd
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
EXTRACTED_TABLES = r"data\extracted_tables"
ALLOWED_EXTENSIONS = {"pdf"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["EXTRACTED_TABLES"] = EXTRACTED_TABLES

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_page_1_data():
    df = pd.read_csv(os.path.join(app.config["EXTRACTED_TABLES"], "page_1_table_1.csv"))
    df.head()
    portfolio_values = str(df.iat[0, 2]).split(" ")  
    portfolio_values.extend([df.iat[0, 0], df.iat[1, 2]])
    portfolio_names  = ["CSDL", "NSDL", "Mutual Fund", "Client", "Total"]
    portfolio_valuation = zip_longest(portfolio_names, portfolio_values, fillvalue="Other")
    return dict(portfolio_valuation)

def get_page_3_table_1_data():
    df = pd.read_csv(os.path.join(app.config["EXTRACTED_TABLES"], "page_3_table_1.csv"))
    # df = pd.read_csv("./newExtractedTable/page_3_table_1.csv")
    df = df.rename(
        columns={'Month-Year -' : "MonthYear", 'Portfolio Valuation (In ) ( )' : "PortfolioValuation"}
        )
    df['PortfolioValuation'] = df['PortfolioValuation'].str.replace(',', '').astype(float)   
    return {"MonthYear":df["MonthYear"].to_list(), "PortfolioValuation" : df["PortfolioValuation"].to_list()}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    data = {"Page1":get_page_1_data(), "LineChartData":get_page_3_table_1_data()}
    return render_template("dashboard.html", data=data)

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
        savetable(filepath, app.config["EXTRACTED_TABLES"])
        return jsonify({"status": "success", "message": f"File uploaded successfully: {file.filename}"})

    return jsonify({"status": "error", "message": "Invalid file format. Only PDFs allowed."})

if __name__ == "__main__":
    app.run(debug=True)
