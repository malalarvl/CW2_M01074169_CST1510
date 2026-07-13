import bcrypt
import sqlite3
import pandas as pd

#hashed using bcrypt
def generate_hash(psw):
    byte_psw = psw.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(byte_psw, salt)
    return hash.decode('utf-8')

#validating hash vs psw
def is_valid_hash(psw, hash):
    hash_ =hash.encode('utf-8')
    byte_psw = psw.encode('utf-8')
    is_valid = bcrypt.checkpw(byte_psw, hash_)
    return is_valid  


#user registration
def register_user():
    name = input('Enter your name: > ')
    password = input('Enter your password: > ')
    hashed_password = generate_hash(password)
    with open('DATA/users.txt', 'a') as f:
        f.write(f'{name},{hashed_password}\n')
    print('User  successfully registered!')

#user login
def log_in_user():
    name = input('Enter your name: > ')
    password = input('Enter your password: > ')
    with open('DATA/users.txt', 'r') as f:
        users = f.readlines()
    for user in users:
        user_name, user_hash = user.strip().split(',')
        if name == user_name and is_valid_hash(password, user_hash):
            return True
    return False

def main():
    while True:
        print('Welcome to the System!')
        print('Choose from the following option:')
        print('1. To Register')
        print('2. To Log in')
        print('3. To Exit')

        choice = input(' > ')

        if choice == '1':
            register_user()
        elif choice == '2':
            if log_in_user():
                print('Login successful!')
            else:
                print('Incorrect log in. Try again.')
        elif choice == '3':
            print('Goodbye!')
            break

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
    conn.close()
    return user

def get_user(conn, name):
    cur = conn.cursor()
    sql = '''SELECT * FROM users WHERE username = ? '''
    param = (name,)
    cur.execute(sql, param)
    user = cur.fetchone()
    conn.close()
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


def migrate_cyber_incidents(conn):
    data = pd.read_csv('DATA/cyber_incidents.csv')
    data.to_sql('cyber_incidents', conn)
    
def migrate_datasets_metadata(conn):
    data = pd.read_csv('DATA/datasets_metadata.csv')
    data.to_sql('datasets_metadata', conn)

def migrate_it_tickets(conn):
    data = pd.read_csv('DATA/it_tickets.csv')
    data.to_sql('it_tickets', conn)

def get_all_cyber_incidents(conn):
    sql = 'SELECT * FROM cyber_incidents'
    data = pd.read_sql(sql, conn)
    conn.close()
    return (data)

def get_all_datasets_metadata(conn):
    sql = 'SELECT * FROM datasets_metadata'
    data = pd.read_sql(sql, conn)
    conn.close()
    return (data)

def get_all_it_tickets(conn):
    sql = 'SELECT * FROM it_tickets'
    data = pd.read_sql(sql, conn)
    conn.close()
    return (data)

conn = sqlite3.connect('DATA/project_data.db')
print(get_all_it_tickets(conn))







