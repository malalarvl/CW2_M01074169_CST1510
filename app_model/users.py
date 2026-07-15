def add_user(conn, name, hash):
    cur = conn.cursor()
    sql = '''INSERT INTO users (username, password_hash) VALUES (?, ?) '''
    param = (name, hash)
    cur.execute(sql, param)
    conn.commit()



def migrate_user(conn):
    with open('DATA/users.txt', 'r') as f:
        users = f.readlines()

    for user in users:
        user_name, user_hash = user.strip().split(',')
        add_user(conn, user_name, user_hash)


def get_all_users(conn):
    cur = conn.cursor()
    sql = '''SELECT * FROM users '''
    cur.execute(sql)
    user = cur.fetchall()
    return user

def get_user(conn, name):
    cur = conn.cursor()
    sql = '''SELECT * FROM users WHERE username = ? '''
    param = (name,)
    cur.execute(sql, param)
    user = cur.fetchone()
    return (user)

def update_user(conn, old_username, new_username):
    cur = conn.cursor()
    sql = 'UPDATE users SET username = ? WHERE username = ?'
    param = (new_username, old_username)
    cur.execute(sql, param)
    conn.commit()

def delete_user(conn, username):
    cur = conn.cursor()
    sql = 'DELETE FROM users WHERE username = ?'
    param = (username,)
    cur.execute(sql, param)
    conn.commit()
