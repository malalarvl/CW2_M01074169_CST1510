"""Run this file to make an admin from username"""
import sqlite3

try:
    conn = sqlite3.connect('DATA/project_data.db')#connect to database
    cursor = conn.cursor()
    username = input("Enter username to make admin: ").strip()#remove unnecesary extra spaces

    if not username:#validate input is not empty
        print("Error: Username cannot be empty.")
    else:#check if user exists before updating
        cursor.execute("SELECT * FROM users WHERE username =?", (username,))
        user = cursor.fetchone()

        if user is None:
            print(f"Error: User '{username}' not found in database.")
        else:#update role to admin
            cursor.execute("UPDATE users SET role = 'admin' WHERE username = ?",(username,))
            conn.commit()
            print(f"{username} is now admin!")
except sqlite3.Error as e:
    print(f"Database error: {e}")#catch database specific errors
except Exception as e:
    print(f"Unexpected error: {e}")#catch any other unexpected errors
finally:
    conn.close()#always close connection even if error occurs
