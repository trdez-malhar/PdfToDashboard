import pandas as pd
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
DB_CONFIG = {
    "drivername": "mssql+pyodbc",
    "username": "sa",
    "password": "Tr$ez@2@25",
    "host": "INPUN-S-MWUAT",
    "port": "1433",  # Default SQL Server port
    "database": "Testing",
    "query": {"driver": "ODBC Driver 17 for SQL Server", "TrustServerCertificate": "yes"},
}

DB_URL = URL.create(**DB_CONFIG)
engine = create_engine(DB_URL)
df = pd.read_csv(r"..\data\datasets\ISIN_SYMBOL_DATASET.csv")
new_columns_names = ["symbol", "company_name", "series", "listing_date", 
                "paid_up_value", "market_lot", "isin", "face_value"]

old_column_names = df.columns

df = df.rename(columns=dict(zip(old_column_names, new_columns_names)))
# Convert `listing_date` to proper datetime format
df["listing_date"] = pd.to_datetime(df["listing_date"], errors='coerce')

# Insert data into SQL Server using SQLAlchemy
df.to_sql('cas_isin_symbol', con=engine, if_exists='append', index=False)

print("Data inserted successfully!")