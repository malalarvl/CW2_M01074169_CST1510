"""
cyber_incidents.py - Cyber incidents dataset queries
Handle migration from CSV and retrieval from SQLite database
"""
import pandas as pd

def migrate_cyber_incidents(conn):
    """
    Migrate/import data from CSV file 'cyber incidents' into the SQLite database.

    Parameters:
    conn: active SQLite database connection

    Returns:
    None
    """
    try:
        data = pd.read_csv('DATA/cyber_incidents.csv') #read the cyber_incidents CSV file
        data.to_sql('cyber_incidents', conn)#load the CSV file into database
    except FileNotFoundError:
        print("Error: cyber_incidents.csv not found")
    except Exception as e:
        print(f"Error migrating cyber incidents: {e}")


def get_all_cyber_incidents(conn):
    """
    Retrieve all cyber incidents from the database

    Parameters:
    conn: active SQLite database connection

    Returns:
    DataFrame: all rows from the cyber_incidents table
    """
    try:
        sql = 'SELECT * FROM cyber_incidents' #select everything from CSV file
        data = pd.read_sql(sql, conn)
        return data
    except Exception as e:
        print(f"Error retrieving cyber incidents: {e}")
        return pd.DataFrame() #return empty DataFrame if the query fail
