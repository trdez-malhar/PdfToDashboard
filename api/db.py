from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import DB_URL
from decimal import Decimal
import json
TABLES = ["cas_users", "cas_users_accounts",
          "cas_asset_allocation", "cas_portfolio_performance", 
          "cas_cdsl_holdings","cas_mf_holdings"]

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
            # print(f"Inserted ID ({primary_key}):", inserted_id)
            session.commit()
            return inserted_id  

        # Bulk insert (returning row count)
        sql = text(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})")
        result = session.execute(sql, records)
        session.commit()
        # print(f"{result.rowcount} records inserted successfully!")
        return result.rowcount  

    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
        return None if primary_key else 0
    finally:
        session.close()



def add_data(pdata):
    # pdata = read_predefined_data()
    try:
        print(pdata)
        user_id = insert_data(TABLES[0], [pdata["client_info"]], primary_key="user_id")
        # print("got user id", user_id)
        # Insert accounts if data exists
        acc_value = pdata.get("accounts", [])
        if acc_value:
            for v in acc_value:
                v.update({"user_id": user_id})
            insert_data(TABLES[1], acc_value)

        # Insert asset allocation if data exists
        acc_value = pdata.get("asset_allocation", [])
        if acc_value:
            for v in acc_value:
                v.update({"user_id": user_id})
            insert_data(TABLES[2], acc_value)
            # print("inserted asset allocation data")

        # Insert portfolio if data exists
        acc_value = pdata.get("portfolio", [])
        if acc_value:
            for v in acc_value:
                v.update({"user_id": user_id})
            insert_data(TABLES[3], acc_value)
            # print("inserted portfolio data")

        # Insert CDSL Holdings if data exists
        acc_value = pdata.get("CDSLHoldings", [])
        if acc_value:
            for v in acc_value:
                v.update({"user_id": user_id})
            insert_data(TABLES[4], acc_value)
            # print("inserted CDSL Holdings data")
        acc_value = pdata.get("MFHoldings", [])
        if acc_value:
            for v in acc_value:
                v.update({"user_id": user_id})
            insert_data(TABLES[5], acc_value)
            # print("inserted CDSL Holdings data")

        return user_id

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
    keys = ["client_info", "accounts", "asset_allocation", "portfolio", "CDSLHoldings", "MFHoldings"]

# Ensure predefined_data is populated only for available keys in cas_data
    for index in range(min(len(cas_data), len(keys))):
        predefined_data[keys[index]] = cas_data[index]

    # print(predefined_data)
   
    return json.dumps(predefined_data, default=lambda x: float(x) if isinstance(x, Decimal) else x)

# get_dashboard_data(24)
