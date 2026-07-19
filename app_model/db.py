"""
db.py - Database connection.
"""
import sqlite3

def get_connection():
    """
    Creates and returns connection to the SQLite database

    Returns:
    sqlite3.Connection: an open connection to project_data.db
    """

    try:
        # 'check_same_thread=False' allows streamlit to use the connection across pages
        conn = sqlite3.connect('DATA/project_data.db', check_same_thread=False)
        return conn
    except sqlite3.Error as e:#catch database specific errors
        print(f"Error connecting to database:{e}")
        return None
