import streamlit as st
from app.Utils.sidebar import render_sidebar

# Hide default multipage navigation
hide_default_pages = """
<style>
div[data-testid="stSidebarNav"] ul {display: none !important;}
div[data-testid="stSidebarNav"] h2 {display: none !important;}
</style>
"""
st.markdown(hide_default_pages, unsafe_allow_html=True)

render_sidebar()

st.title("⚙️ Settings")
st.subheader("User configuration settings here.")

# -------------------- Theme Toggle --------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if st.button("Toggle Dark / Light Mode"):
    st.session_state.dark_mode = not st.session_state.dark_mode

# Apply theme CSS
dark_css = """
<style>
body, .stApp {background-color: #0e1117; color: #f0f0f0;}
.stButton>button {background-color: #262730; color: #f0f0f0;}
.stSidebar {background-color: #1e1f29; color: #f0f0f0;}
</style>
"""
light_css = """
<style>
body, .stApp {background-color: #ffffff; color: #000000;}
.stButton>button {background-color: #e0e0e0; color: #000000;}
.stSidebar {background-color: #f8f8f8; color: #000000;}
</style>
"""
st.markdown(dark_css if st.session_state.dark_mode else light_css, unsafe_allow_html=True)

# -------------------- Account Settings --------------------
if "user" not in st.session_state:
    st.session_state.user = {
        "username": "guest",
        "password": "1234",
        "domain": "Cyber",
        "timezone": "UTC",
        "language": "English"
    }

if "users" not in st.session_state:
    st.session_state.users = {}  # {username: {password, role}}

user = st.session_state.user
users = st.session_state.users

st.subheader("👤 Account Settings")
new_username = st.text_input("Change Username", value=user["username"])
new_password = st.text_input("Change Password", value=user["password"], type="password")

if st.button("Save Account Changes"):
    old_username = user["username"]
    
    # Update session_state.user
    user["username"] = new_username
    user["password"] = new_password
    st.session_state.user = user

    # Sync to session_state.users
    if old_username in users:
        # Remove old entry and add new
        users.pop(old_username)
    users[new_username] = {"password": new_password, "role": users.get(old_username, {}).get("role", "cyber")}
    st.session_state.users = users

    st.success("Account details updated successfully! You must log in again.")
    st.session_state.logged_in = False
    st.switch_page("pages/login.py")

# -------------------- Clear AI Chat History --------------------
st.subheader("🧹 AI Assistant")
if st.button("Clear AI Chat History"):
    st.session_state.messages = []
    st.success("AI chat history cleared!")
