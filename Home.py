"""
Home.py - Main entry point for the streamlit application
Provides login and registration tabs with input validation
and secure bcrypt password hashing
"""
import streamlit as st
from app_model.hashing import generate_hash, is_valid_hash
from app_model.db import get_connection
from app_model.users import add_user, get_user

#etablish database connection on page load
conn = get_connection()


st.set_page_config(page_title="Home", page_icon="🏡", layout="wide")

st.title("Welcome to the main page ")

#initialise session state - tracks login status across pages
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

tab_login, tab_register = st.tabs(["Login", "Register"])

#LOGIN TABS
with tab_login:
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log In"):
        #Validate fields are not empty
        if not login_username or not login_password:
            st.error("Please fill in all fields.")
        else:
            try:
                user = get_user(conn, login_username)#search database for user
                if user is None:
                    st.error("User not found")#user name does not exist
                else:
                    id, user_name, user_hash, role = user

                    if is_valid_hash(login_password, user_hash):#verify password
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = user_name
                        st.session_state['role'] = role

                        st.success("Logged in sucessfully!")
                        st.switch_page("pages/1_Dashboard.py")
                    else:
                        st.error("Incorrect password")#password does not match
            except Exception as e:
                st.error(f"Login error: {e}")#catch unexpected errors

#REGISTER TAB
with tab_register:
    register_username = st.text_input("New Username")
    register_password = st.text_input("New Password", type="password")
    if st.button("Register"):
        #validate all fields are filled
        if register_username == "" or register_password == "":
            st.error("Please fill in all fields.")
        #validate password requirements
        elif len(register_password) < 8 :
            st.error("Password must contain at least 8 characters.")
        elif not any(char.isdigit() for char in register_password):
            st.error("Password must contain at least one number.")
        elif not any(char.isupper() for char in register_password):
            st.error("Password must contain at least one uppercase letter.")

        else:
            try:
                existing = get_user(conn, register_username)
                
                if existing : st.error("Username already exists.")#prevent duplicate username
                else:
                    hashed_password = generate_hash(register_password)#hash before storing
                    add_user(conn, register_username, hashed_password)
                    st.success("Registration succesfull!")
            except Exception as e:
                st.error(f"Registration error: {e}")#catch unexpected errors

