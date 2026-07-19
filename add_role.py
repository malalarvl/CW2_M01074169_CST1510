"""Run this file to make an admin from username"""
import sqlite3
conn = sqlite3.connect('DATA/project_data.db')
cursor = conn.cursor()

username = input("Enter username to make admin: ")

cursor.execute("UPDATE users SET role = 'admin' WHERE username =?", (username,))

conn.commit()
conn.close()
print(f"{username} is now admin!")