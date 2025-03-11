from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import DB_URL

# Create database engine
engine = create_engine(DB_URL, echo=False, isolation_level="AUTOCOMMIT", connect_args={"timeout": 10})

# Create a session factory
SessionLocal = sessionmaker(bind=engine)

def insert_data_bulk(table_name, records):
    """
    Insert multiple records into a table using a bulk insert with SQLAlchemy.
    
    :param table_name: Name of the table
    :param records: List of dictionaries with column-value pairs
    :return: Number of rows inserted
    """
    session = SessionLocal()
    try:
        if not records:
            print("No data to insert.")
            return 0
        
        # Extract column names dynamically from the first record
        columns = ", ".join(records[0].keys())  
        
        # Create named placeholders dynamically
        placeholders = ", ".join(f":{col}" for col in records[0].keys())

        # Construct SQL query
        sql = text(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})")
        print(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})")
        # Execute bulk insert
        # result = session.execute(sql, records)  # `records` is a list of dictionaries
        # print("call")
        # session.commit()  # Commit transaction

        # print(f"{result.rowcount} records inserted successfully!")
        # return result.rowcount  # Return number of affected rows
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()  # Rollback if error occurs
        return None
    finally:
        session.close()

def read_predefined_data():
    import json
    with open(r"C:\Users\malhar.yadav\scripts\PdfToDashboard\final_data_MSY.json", mode="r", encoding="utf-8") as fp:
        pdata = json.loads(fp.read())
    return pdata
# print(read_predefined_data())

def add_data():
    pdata = read_predefined_data()

