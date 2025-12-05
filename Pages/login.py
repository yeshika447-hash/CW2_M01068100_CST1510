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

# Render shared sidebar
render_sidebar()

st.set_page_config(page_title="Login / Register", page_icon="🔑", layout="centered")

# ---------- Initialise session state ----------
if "users" not in st.session_state:
    st.session_state.users = {}   # {username: {password, role}}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = None


st.title("🔐 Welcome")

# If already logged in
if st.session_state.logged_in:
    st.success(f"Already logged in as **{st.session_state.username}**.")
    if st.button("Go to dashboard"):
        st.switch_page("pages/1_Dashboard.py")
    st.stop()


# ---------- Tabs ----------
tab_login, tab_register = st.tabs(["Login", "Register"])

# ----- LOGIN TAB -----
with tab_login:
    st.subheader("Login")

    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")

    if st.button("Log in", type="primary"):
        users = st.session_state.users

        if (
            login_username in users
            and users[login_username]["password"] == login_password
        ):
            st.session_state.logged_in = True
            st.session_state.username = login_username
            st.session_state.role = users[login_username]["role"]

            st.session_state.user = {
                "username": login_username,
                "password": users[login_username]["password"],
                "role": users[login_username]["role"],
                "timezone": "UTC",
                "language": "English",
            }

            st.success("Login successful!")
            st.switch_page("pages/1_Dashboard.py")


# ----- REGISTER TAB -----
with tab_register:
    st.subheader("Register")

    new_username = st.text_input("Choose a username")
    new_password = st.text_input("Choose a password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")
    new_role = st.selectbox("Choose your domain role", ["cyber", "datascience", "it"])

    if st.button("Create account"):
        if not new_username or not new_password:
            st.warning("Fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        elif new_username in st.session_state.users:
            st.error("Username already exists.")
        else:
            st.session_state.users[new_username] = {
                "password": new_password,
                "role": new_role,
            }

            # Create user session object
            st.session_state.user = {
            "username": new_username,
            "password": new_password,
            "role": new_role,
            "timezone": "UTC",
            "language": "English",
        }
    st.success("Account created! You can now log in.")

