"""
schema.py - Database schema creation
Creates all required table in sqlite database
"""
def create_user_table(conn):
    """
    Create the users table if it does not already exist yet

    Parameters:
    conn: SQLite database connection
    """
    try:
        cur = conn.cursor()
        sql = '''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user'
        );  
        ''' # IF NOT EXISTS prevents crash if table exists
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print(f"Error creating users table: {e}")


