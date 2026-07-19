CST1510 Coursework 2

Secure Multidomain Intelligence Platform

Student ID: M01074169

A secure web application built with Python and Streamlit that provides
user authentication, interactive data visualisation across three datasets,
and an AI assistant powered by the Groq API

Technologies Used:
bcrypt
sqlite3
pandas
streamlit
groq

How to Run:
-Step 1 — Clone the repository
git clone https://github.com/malalarvl/CW2_M01074169_CST1510.git
cd CW2_M01074169_CST1510

-Step 2 — Create and activate a virtual environment
python -m venv .venv

*Windows
.venv\Scripts\activate

*Mac/Linux
source .venv/bin/activate

-Step 3 — Install all dependencies
pip install -r requirements.txt

-Step 4 — Set up your Groq API key
Go to https://console.groq.com and sign up for a free account
Generate a free API key
Add your API key 'client = Groq(api_key="Add your API key here")'

-Step 5 — Run the application
Go to 'Dashboard.py' and run on terminal 'streamlit run Home.py'

-Default Test Account
Register a new account on the login page where each user are assigned as 'user' by default.
An admin account can be set up by running 'add_role.py' file and entering username
Or by user name: 'Admin' and password: 'Admin123'