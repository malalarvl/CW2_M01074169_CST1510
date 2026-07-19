"""
it_tickets.py - IT tickets dataset queries
Handles migration from CSV and retrieval from SQLite database
"""
import pandas as pd

def migrate_it_tickets(conn):
    """
    Migrates IT tickets data from CSV file into the SQLite database

    Parameters:
    conn: SQLite database connection
    """

    try:  
        data = pd.read_csv('DATA/it_tickets.csv')#read csv file
        data.to_sql('it_tickets', conn)#load data from csv file into database
    except FileNotFoundError:
        print("Error: it_tickets.csv not found")
    except Exception as e:
        print(f"Error migrating IT tickets: {e}")


def get_all_it_tickets(conn):
    """
    Retrieve all IT  tickects from the database

    Parameters:
    conn: active SQLite database connection

    Returns:
    DataFrame: all row from it_tickets table
    """
    try:
        sql = 'SELECT * FROM it_tickets'#select everything from CSV file
        data = pd.read_sql(sql, conn)
        return data
    except Exception as e:
        print(f"Error retrieving IT tickets: {e}")
        return pd.DataFrame()#return empty DataFrame if query fails