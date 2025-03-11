import os
import re
import unicodedata
import pandas as pd
from config import ALLOWED_EXTENSIONS

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def dataframe_to_dict(df):
    """Convert a DataFrame to a nested dictionary."""
    dict_key_column = df.columns[0]
    df = df.dropna(subset=[dict_key_column])
    return [row.to_dict() for _, row in df.iterrows()]

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
