"""
1_Dashboard.py - dashboard using streamlit
Displays cyber incidents, IT tickets and dataset metadata
Allows authenticated and access their profile
Administrators can also manage registered users 
"""
import streamlit as st
from app_model.cyber_incidents import get_all_cyber_incidents
from app_model.it_tickets import get_all_it_tickets
from app_model.metadatas import get_all_datasets_metadata
from app_model.db import get_connection
from app_model.users import get_all_users, delete_user

import pandas as pd

#set up the page
st.set_page_config(page_title="Home", page_icon="🏡", layout="wide")

#Etablish a connection to the SQLite database
conn = get_connection()


if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

#Prevent users from accessing the dashboard unless they are logged in
if not st.session_state['logged_in']:
    st.warning("Please log in to access to dashboard.")  
    if st.button("Go to Login Page"):
        st.switch_page("Home.py")
    st.stop()
else:
    st.success("You are logged in!")


try: #store imported function for better and easy use
    data = get_all_cyber_incidents(conn)
    tickets = get_all_it_tickets(conn)
    metadata = get_all_datasets_metadata(conn)
except Exception as e:
    st.error(f"Error loading dashboard data: {e}")
    st.stop()

st.title("Welcome to the Cyber Incidents Dashboard ")

#Sidebar containing filters and navigation options
with st.sidebar:
    #add filters for cyber incidents and it tickets to the side bar
    st.header("Filters")

    st.subheader("Cyber Incidents")
    severity_ = st.selectbox('Severity level', ['All'] + list(data['severity'].unique()))
    category_ = st.selectbox('Category level', ['All'] + list(data['category'].unique()))
    status_ = st.selectbox('Status level', ['All'] + list(data['status'].unique()))
    st.divider()

    st.subheader("IT Tickets")
    priority_ = st.selectbox('Priority', ['All'] + list(tickets['priority'].unique()))
    tickets_status_ = st.selectbox('Status level', ['All'] + list(tickets['status'].unique()))
    st.divider()

    #add 'My profile' button to the side bar
    if st.button("My Profile"):
        st.switch_page("pages/2_Profile_page.py")

     #add 'log out' button to the side bar
    if st.button("Log Out"):
        st.session_state.clear()
        st.switch_page("Home.py")

#Apply the selected filters to the cyber incidents datasets
filtered_data = data.copy()
if severity_ != 'All':#Allow users to filters cyber incident by severity level
    filtered_data  = filtered_data[filtered_data['severity'] == severity_]
if category_ != 'All':#Allow users to filters cyber incident by category
    filtered_data  = filtered_data[filtered_data['category'] == category_]
if status_ != 'All':#Allow users to filters cyber incident by status
    filtered_data  = filtered_data[filtered_data['status'] == status_]

#Apply the selected filters to the IT tickets datasets
filtered_tickets = tickets.copy()
#Allow users to filters it tickets by priority level
if priority_ != 'All':
    filtered_tickets  = filtered_tickets[filtered_tickets['priority'] == priority_]
#Allow users to filters it tickets by status
if tickets_status_ != 'All':
    filtered_tickets  = filtered_tickets[filtered_tickets['status'] == tickets_status_]

#display dashboard information in separate tabs
tab1, tab2, tab3 = st.tabs(["Cyber Incidents", "IT Tickets", "Metadata"])

with tab1:
    st.subheader("Cyber Incidents")

    data['timestamp'] = pd.to_datetime(data['timestamp'])
    filtered_data['timestamp'] = pd.to_datetime(filtered_data['timestamp'])

    col1,col2 = st.columns(2)
    with col1:
        st.subheader(f"Incidents by Category")
        st.bar_chart(filtered_data['category'].value_counts())
    with col2:
        st.subheader("Category Trend Over Time")
        st.line_chart(filtered_data, x= 'timestamp', y='category')

    st.subheader("Filtered Data")
    st.dataframe(filtered_data)
    st.download_button(label="Download as CSV", 
                       data=filtered_data.to_csv(index=False),
                       file_name=f"cyber_incidents_{severity_}.csv",
                       mime="text/csv")#download button to save filtered data as csv file
    
with tab2:
    st.subheader("IT Tickets")

    st.bar_chart(filtered_tickets['priority'].value_counts())
    st.dataframe(filtered_tickets)
    st.download_button(label="Download as CSV", 
                       data=filtered_tickets.to_csv(index=False),
                       file_name=f"it_tickets_filtered.csv",
                       mime="text/csv")#download button to save filtered data as csv file

with tab3:#no filter and download button as data are few
    st.subheader("Datasets Metadata")
    st.dataframe(metadata)

#Only administrators can manage registered users
if st.session_state.get('role') == 'admin':
    st.divider()

    st.markdown("Admin Panel")
    st.caption("All registered users")
    all_users = get_all_users(conn)

    st.info(f"Total users: {len(all_users)}")

    #set columns for username, role and action
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.markdown("Username")
    with col2:
        st.markdown("Role")
    with col3:
        st.markdown("Action")

    st.divider()

    for user in all_users:#loop through every users or admin to be displayed in admin pannel
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.write(f"{user[1]}")
        with col2:
            if user[3] == 'admin':
                st.markdown("Admin")
            else:
                st.markdown("User")

        with col3:
            #prevent admin from deleting themlselves
            if user[1] == st.session_state.get('username'):
                st.button("locked",key=f"del_{user[0]}", disabled=True)
            else:
                
                if st.button(f"Delete", key=f"del_{user[0]}"):
                    try:#delete user
                        delete_user(conn, user[1])
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting user: {e}")
