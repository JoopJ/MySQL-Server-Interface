import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# ------------------- Database Functions ------------------- # 

def create_connection():
    load_dotenv()
    connection = None
    
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        print("Connection to MySQL successful")
    except Error as e:
        print(f"Error: '{e}'")
    
    return connection

def execute_query(connection, query):
    try:
        connection.cursor().execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"Error: '{e}'")
    finally:
        connection.cursor().close()
        
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except Error as e:
        print(f"Error: '{e}'")
    finally:
        cursor.close()
        return result

# ------------------^ Database Functions ^------------------ #

# --------------------- Common Queries --------------------- #

def show_databases(connection):
    query = "SHOW DATABASES"
    return read_query(connection, query)

def show_tables(connection):
    query = "SHOW TABLES"
    return read_query(connection, query)

def use_database(connection, database):
    query = f"USE {database}"
    execute_query(connection, query)
    
# --------------------^ Common Queries ^-------------------- #

# ---------------------- Specialized ----------------------- #

def list_databases(connection):
    databases = show_databases(connection)
    return [db[0] for db in databases]

# ---------------------^ Specialized ^---------------------- #