"""
users.py - User CRUD operations
Handles all database operations for the users table including
registration,login verification,update and deletion
"""
def add_user(conn, name, hash, role="user"):
    """
    Insert a new user into the users table

    Parameters:
    conn: active SQLite database connection
    name: username to register
    hashed: bcrypt hashed password
    role: user role
    """
    try:
        cur = conn.cursor()
        sql = '''INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?) ''' #add the new name,hashed password,role of the new user
        param = (name, hash, role)
        cur.execute(sql, param)
        conn.commit()
    except Exception as e:
        print(f"Error adding user:{e}")



def migrate_user(conn):
    """
    Migrate users from the text file into sqlite database
    Reads 'users.txt' and inserts each users into the users table

    Parameters:
    conn: active SQLite database connection
    """
    try:
        with open('DATA/users.txt', 'r') as f:
            users = f.readlines() #read all lines from 'users.text'

        for user in users: #loop through each new users and add to database
            user_name, user_hash = user.strip().split(',')
            add_user(conn, user_name, user_hash)
    except FileNotFoundError:
        print("Error : users.txt not found")
    except Exception as e:
        print(f"Error migrating users: {e}")



def get_all_users(conn):
    """
    Retrieve all users from the database
    
    Parameters:
    conn: active SQLite database connection
    
    Returns:
    list: all rows from the users table
    """
    try:
        cur = conn.cursor()
        sql = '''SELECT * FROM users '''
        cur.execute(sql)
        user = cur.fetchall()
        return user
    except Exception as e:
        print(f"Error retrieving users: {e}")
        return []#return empty list if query fails

def get_user(conn, name):
    """
    Retrieve a single user from the database by username
    Search is case insensitive

    Parameters:
    conn: active SQLite database connection
    name: username to search for

    Returns:
    Tuple: user row as (id, username,password_hash,role) or none if not found
    """
    try:
        cur = conn.cursor()
        sql = '''SELECT * FROM users WHERE username = ? COLLATE NOCASE'''#case insensitive search
        param = (name,)
        cur.execute(sql, param)
        user = cur.fetchone()
        return (user)
    except Exception as e:
        print(f"Error retrieving user: {e}")
        return None


def update_user(conn, old_username, new_username):
    """
    Update an user's name in database
    Return false if the new username already exist

    Parameters:
    conn: active SQLite database connection
    old_username:current username
    new_username:new username to set

    Returns:
    True if updated successfully
    
    """
    try:
        if get_user(conn, new_username):#check if new username already taken
            return False
        cur = conn.cursor()
        sql = 'UPDATE users SET username = ? WHERE username = ?' #update the new username to the database by the current user name
        param = (new_username, old_username)
        cur.execute(sql, param)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating username: {e}")
        return False

def delete_user(conn, username):
    """
    Delete a user from database by username
    
    Parameters:
    conn: active SQLite database connection
    username: username of the user to delete
    """
    try:
        cur = conn.cursor()
        sql = 'DELETE FROM users WHERE username = ?'#delete an user to the database by the current user name
        param = (username,)
        cur.execute(sql, param)
        conn.commit()
    except Exception as e:
        print(f"Error deleting user: {e}")

def update_password(conn, username, new_hash):
    """
    Update a user's password hash in the database
    
    Parameters:
    conn: active SQLite database connection
    username: username of the user to update
    new_hash: new bcrypt hashed password"""
    try:
        cur = conn.cursor()

        sql = '''
        UPDATE users
        SET password_hash = ?
        WHERE username = ? 
        ''' #update the password to the database by the current user name

        param = (new_hash, username)

        cur.execute(sql, param)
        conn.commit()
    except Exception as e:
        print(f"Error updating password: {e}")