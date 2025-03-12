from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import DB_URL
from decimal import Decimal
TABLES = ["cas_users", "cas_users_accounts",
          "cas_asset_allocation", "cas_portfolio_performance", 
          "cas_cdsl_holdings"]

# # Create database engine
engine = create_engine(DB_URL, echo=False, isolation_level="AUTOCOMMIT", connect_args={"timeout": 10})

# # Create a session factory
SessionLocal = sessionmaker(bind=engine)

def insert_data(table_name, records, primary_key=None):
    """
    Inserts records into a table. 
    - If `primary_key` is provided, returns the inserted primary key (for single record insert).
    - If `primary_key` is None, performs a bulk insert and returns the number of rows inserted.

    :param table_name: Name of the table
    :param records: List of dictionaries with column-value pairs
    :param primary_key: The primary key column to be returned (for single insert)
    :return: Inserted primary key (if primary_key is provided) or number of rows inserted
    """
    session = SessionLocal()
    try:
        if not records:
            print("No data to insert.")
            return None if primary_key else 0

        # Extract column names dynamically
        columns = ", ".join(records[0].keys())  
        placeholders = ", ".join(f":{col}" for col in records[0].keys())

        # Single record insert (returning primary key)
        if primary_key and len(records) == 1:
            sql = text(f"INSERT INTO {table_name} ({columns}) OUTPUT INSERTED.{primary_key} VALUES ({placeholders})")
            result = session.execute(sql, records)
            inserted_id = result.scalar()
            print(f"Inserted ID ({primary_key}):", inserted_id)
            session.commit()
            return inserted_id  

        # Bulk insert (returning row count)
        sql = text(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})")
        result = session.execute(sql, records)
        session.commit()
        print(f"{result.rowcount} records inserted successfully!")
        return result.rowcount  

    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
        return None if primary_key else 0
    finally:
        session.close()


def read_predefined_data():
    import json
    with open(r"C:\Users\malhar.yadav\scripts\PdfToDashboard\final_data_Shriraj Devidas Bhore.json", mode="r", encoding="utf-8") as fp:
        pdata = json.loads(fp.read())
    return pdata
# print(read_predefined_data())

def add_data(pdata):
    # pdata = read_predefined_data()
    try:
        user_id = insert_data(TABLES[0],[pdata["client_info"]], primary_key="user_id")
        print("got user id",user_id)
        acc_value = pdata["accounts"]
        for v in acc_value:
            v.update({"user_id" : user_id})
        for accs in acc_value:
            acc_id = insert_data(TABLES[1],[accs], primary_key="account_id")
            print("got acc id",acc_id)
        print("insert bulk data")
        acc_value = pdata["asset_allocation"]
        for v in acc_value:
            v.update({"user_id" : user_id})
        insert_data(TABLES[2],acc_value, primary_key="user_id")
        print("insert bulk data")
        acc_value = pdata["portfolio"]
        for v in acc_value:
            v.update({"user_id" : user_id})
        insert_data(TABLES[3],acc_value, primary_key="user_id")
        print("insert bulk data")
        acc_value = pdata["CDSLHoldings"]
        for v in acc_value:
            v.update({"user_id" : user_id})
        insert_data(TABLES[4], acc_value, primary_key="user_id")
        return True
    except Exception as err:
        print("Error while inserting data : ", err)
        return None

# add_data()
def call_stored_procedure_multi(user_id):
    session = SessionLocal()
    try:
        with session.connection() as conn:
            result = conn.execute(text("EXEC cas_get_data :user_id"), {"user_id": user_id})
            results = []
            cursor = result.cursor  # Get raw DBAPI cursor

            while cursor:
                columns = [desc[0] for desc in cursor.description]  # Extract column names
                rows = cursor.fetchall()

                if rows:  # Avoid appending empty sets
                    results.append([dict(zip(columns, row)) for row in rows])

                if not cursor.nextset():  # Move to the next result set
                    break

            return results
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        session.close()

# Call the stored procedure

def get_dashboard_data(user_id):
    
    predefined_data = {
        "client_info": {"name": None},
        "accounts": None,
        "asset_allocation": None,
        "portfolio": None,
        "CDSLHoldings": None,
        "MFHoldings": None,
    }
    cas_data = call_stored_procedure_multi(user_id)
    predefined_data["client_info"] = cas_data[0]
    predefined_data["accounts"] = cas_data[1]
    predefined_data["asset_allocation"] = cas_data[2]
    predefined_data["portfolio"] = cas_data[3]
    predefined_data["CDSLHoldings"] = cas_data[4]
    print(predefined_data)
    import json
    with open("newstruct_data.json", mode="w", encoding="utf-8") as fp:
        json.dump(predefined_data, fp, indent=4, default=lambda x: float(x) if isinstance(x, Decimal) else x)

get_dashboard_data(24)
