"""
2_Profile_page.py - User profile management page
Allows logged-in users to views details, update username
change password and log out
"""

import streamlit as st
from app_model.db import get_connection
from app_model.users import get_user , update_user, update_password
from app_model.hashing import generate_hash, is_valid_hash

st.set_page_config(page_title="Profile", page_icon="👤", layout="wide")

#redirect to login if not yet authenticated
if not st.session_state.get('logged_in'):
    st.warning("Please log in first.")
    st.switch_page("Home.py")
    st.stop()
try:
    conn = get_connection()
    user = get_user(conn, st.session_state['username'])

    if user is None:
        st.error("User not found.Please log in again")
        st.session_state.clear()
        st.stop()
    id, username, password_hash, role = user
except Exception as e:
    st.error(f"Error loading profile:{e}")
    st.stop()

#HEADER
st.title("My Profile")
st.divider()

#CURRENT DETAILS
st.subheader("Current Details")
col1, col2, col3 = st.columns(3) #set 03 columns for username,account id and role
with col1:
    st.metric(label="Username", value=username)
with col2:
    st.metric(label="Account ID", value=f"#{id}")
with col3:
    if role == 'admin':
        st.metric(label="Role",value="Admin")
    else:
        st.metric(label="Role",value="User")
st.divider()

#UPDATE USERNAME
st.subheader("Update Username")
st.caption("Change your username.")
new_username = st.text_input("New Username", placeholder="Enter new username")

if st.button("Update Username"):
    if new_username == "":#Validate input before updating
        st.error("Please enter a new username.")
    elif new_username == username:#check if current and new username are not the same
        st.error("New username is the same as current username.")
    else:
        try:
            updated =  update_user(conn, username, new_username)
            if updated:#update valid new username
                st.session_state['username'] = new_username
                st.success(f"Username updated to {new_username}!")
            else:#error message if new username already exist
                st.error("Username already exists.")
        except Exception as e:
            st.error(f"Error updating username: {e}")

st.divider()

#CHANGE PASSWORD
st.subheader("Change Password")
st.caption("Enter your current password then set a new one")

current_password = st.text_input("Current Password", type="password")
new_password = st.text_input("New Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")

if st.button("Change Password"):
    #validate all fields filled
    if not current_password or not new_password or not confirm_password:
        st.error("Please fill in all fields.")
    #verify current password is correct
    if not is_valid_hash(current_password, password_hash):
        st.error("Current password is incorrect.")
    #validate new password requirements
    elif new_password != confirm_password:
        st.error("New Password and Confirmed Password do not match.")
    elif len(new_password) < 8 :
        st.error("Password must contain at least 8 characters.")
    elif not any(char.isdigit() for char in new_password):
        st.error("Password must contain at least one number.")
    elif not any(char.isupper() for char in new_password):
        st.error("Password must contain at least one uppercase letter.")
    else:
        try:
            new_hash = generate_hash(new_password)#hash before storing
            update_password(conn, username, new_hash)
            st.success("Password updated successfully")
        except Exception as e:
            st.error(f"Error updating password: {e}")
st.divider()

#LOG OUT
if st.button("Log Out"):
    st.session_state.clear()#clear all session data
    st.switch_page("Home.py")

