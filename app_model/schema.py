def create_useer_table(conn):
    cur = conn.cursor()
    sql = '''CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL
    );
    '''
    cur.execute(sql)
    conn.commit()