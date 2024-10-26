import streamlit as st
import requests  # For interacting with backend APIs

# Set page config with SolarShare branding
st.set_page_config(page_title="SolarShare", layout="centered", page_icon="☀️")

# Initialize session state for tracking login inputs and navigation
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'
if 'user_type' not in st.session_state:
    st.session_state['user_type'] = None
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'password' not in st.session_state:
    st.session_state['password'] = ""

# Function to switch pages
def switch_page(page):
    st.session_state['page'] = page
    st.experimental_rerun()

# Function to call APIs
def api_call(endpoint, data):
    url = f"http://localhost:8000/api/{endpoint}"  # Replace with your backend URL
    response = requests.post(url, json=data)
    return response

# Login Form
def login_form(user_type):
    st.header(f"Login to SolarShare as {user_type.capitalize()}")

    # Input fields with session state tracking
    st.session_state['username'] = st.text_input(
        "Username", 
        value=st.session_state['username'], 
        placeholder="Enter your username"
    )
    st.session_state['password'] = st.text_input(
        "Password", 
        value=st.session_state['password'], 
        placeholder="Enter your password", 
        type="password"
    )

    if st.button("Login"):
        response = api_call(f"login-{user_type}", {
            "username": st.session_state['username'],
            "password": st.session_state['password']
        })

        if response.ok:
            st.session_state['logged_in'] = True
            st.session_state['user_type'] = user_type
            switch_page("home")
        else:
            st.error("Login failed. Please try again.")

# Registration Form
def register_form():
    st.header("Join SolarShare")
    username = st.text_input("Username", placeholder="Create a username")
    password = st.text_input("Password", placeholder="Create a password", type="password")
    if st.button("Register"):
        response = api_call("register", {"username": username, "password": password})
        if response.ok:
            st.success("Registration successful! Please log in.")
        else:
            st.error("Registration failed. Try again.")

# Home Page
def home_page():
    st.title(f"Welcome to SolarShare, {st.session_state['user_type'].capitalize()}!")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Buy Subscription"):
            st.success("Subscription purchased!")

    with col2:
        if st.button("View Ongoing Solar Projects"):
            projects = api_call("projects", {}).json()
            st.subheader("Ongoing Projects")
            for project in projects:
                st.markdown(f"🔆 **{project['name']}**")

    with col3:
        if st.button("Get Recommendations"):
            recommendations = api_call("recommendations", {}).json()
            st.subheader("Recommended Projects")
            for rec in recommendations:
                st.markdown(f"✨ **{rec['name']}**")

    if st.button("Logout"):
        st.session_state['logged_in'] = False
        switch_page("login")

# Main Function to Control Page Flow
def main():
    st.markdown(
        """
        <style>
        .css-18e3th9 {
            padding-top: 2rem;
            padding-bottom: 10rem;
        }
        .stButton>button {
            width: 100%;
            font-size: 1.2rem;
            border-radius: 10px;
            background-color: #ffa726;
            color: white;
        }
        .stButton>button:hover {
            background-color: #fb8c00;
        }
        </style>
        """, unsafe_allow_html=True
    )

    if st.session_state['page'] == 'login':
        st.title("SolarShare")
        st.subheader("Powering Communities with Renewable Energy")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Login as Community"):
                login_form("community")

        with col2:
            if st.button("Login as Company"):
                login_form("company")

        st.write("Don't have an account?")
        if st.button("Register Now"):
            register_form()
    elif st.session_state['page'] == 'home':
        home_page()

# Run the App
if __name__ == "__main__":
    main()
