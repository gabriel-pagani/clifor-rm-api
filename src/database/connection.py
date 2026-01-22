import pyodbc
import os
from dotenv import load_dotenv


load_dotenv()

def get_connection() -> pyodbc.connect:
    connection_string = f"DRIVER={{SQL Server}}; SERVER={os.getenv("SERVER_IP")}; DATABASE={os.getenv("SERVER_DATABASE")}; UID={os.getenv("SERVER_USER")}; PWD={os.getenv("SERVER_PWD")}"
    return pyodbc.connect(connection_string)


def execute_query(query: str) -> dict:
    try:
        with get_connection().cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
            return data

    except Exception as e:
        print(f"request-exception: {e}")
