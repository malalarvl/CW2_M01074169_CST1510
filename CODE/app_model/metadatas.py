"""
metadatas.py - metadatas dataset queries
Handles migration from CSV and retrieval from SQLite database
"""
import pandas as pd

def migrate_datasets_metadata(conn):
    """
    Migrates IT tickets data from CSV file into the SQLite database

    Parameters:
    conn: SQLite database connection
    """
    try:
        data = pd.read_csv('DATA/datasets_metadata.csv')
        data.to_sql('datasets_metadata', conn)

    except FileNotFoundError:
        print("Error: metadatas.csv not found")
    except Exception as e:
        print(f"Error migrating datasets metadata: {e}")

def get_all_datasets_metadata(conn):
    """
    Retrieve all dataset metadatas from the database

    Parameters:
    conn: active SQLite database connection

    Returns:
    DataFrame: all row from datasets_metadata table
    """
    try:
        sql = 'SELECT * FROM datasets_metadata'#select everything from CSV file
        data = pd.read_sql(sql, conn)
        return data
    except Exception as e:
        print(f"Error retrieving datasets metadata: {e}")
        return pd.DataFrame()#return empty DataFrame if query fails