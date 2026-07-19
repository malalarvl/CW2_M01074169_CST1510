"""
main.py - Terminal-based entry point for the application
Provides a simple command-line interface for registering
and logging in users before the Streamlit dashboard was built
"""

from app_model.db import get_connection
from app_model.users import add_user , get_user
from app_model.hashing import generate_hash, is_valid_hash

#etablish database connection
conn = get_connection()


#user registration
def register_user(conn):
    """
    Register a new user via terminal input.
    
    Parameters:
    conn: active sqlite database connection"""
    name = input('Enter your name: > ')
    password = input('Enter your password: > ')

    try:
        existing = get_user(conn, name)
        if existing:
            print("Username already exists")
            return
        
        hashed_password = generate_hash(password)#hash before storing
        add_user(conn, name, hashed_password)
        print("User registered successfully!")

    except Exception as e:
        print(f"Error registering user: {e}")

#user login
def log_in_user(conn):
    """
    Log in an existing user via terminal input

    Parameters:
    conn: active sqlite database connection

    Returns: 
    True if login successful,false if not
    """
    name = input('Enter your name: > ')
    password = input('Enter your password: > ')
    try:
        user = get_user(conn, name)

        if user is None:
            print("User not found")
            return False
        
        id, user_name, user_hash, role = user
       
        if is_valid_hash(password, user_hash):#verify password
                print(f'Welcome {user_name}!')
                return True
        
        print("Incorrect password.")
        return False
    
    except Exception as e:
        print(f"Error logging in: {e}")
        return False

def main():
    """
    Main loop - displays menu and handles user choices
    """
    while True:
        print('Welcome to the System!')
        print('Choose from the following option:')
        print('1. To Register')
        print('2. To Log in')
        print('3. To Exit')

        choice = input(' > ')

        if choice == '1':
            register_user(conn)
        elif choice == '2':
            if log_in_user(conn):
                print('Login successful!')
            else:
                print('Incorrect log in. Try again.')
        elif choice == '3':
            print('Goodbye!')
            break
        else:
            print("Invalid choice.Please enter 1,2, or 3.")#handle invalid input

if __name__ == '__main__':
    main()

