import streamlit as st
from app.Data.users import get_all_users
from app.Services.user_service import migrate_users_from_file
from app.Data.db import connect_database
from app.Data.incidents import get_all_incidents

# PAGE CONFIG
st.set_page_config(page_title="Multi-domain Platform", page_icon="🎓", layout="wide")

# DATABASE CONNECTION
conn = connect_database()

# Initialize show_users in session state
if "show_users" not in st.session_state:
    st.session_state.show_users = False

# MAIN PAGE CONTENT
st.title("Multi-domain Intelligence Platform")
st.write("Welcome! Click below to continue.")
if st.button("Go to Login Page"):
    st.switch_page("pages/login.py")

# USERS SECTION
with st.sidebar:
    if st.button("👤 View Users"):
        st.session_state.show_users = not st.session_state.show_users

    conn = connect_database()

    st.subheader("👤 Registered Users")
    df = get_all_incidents(conn)
    print(f"Total incidents: {len(df)}")

    migrate_users_from_file()
    df = get_all_users()
    safe_cols = ["id", "username", "role"]
    df = df[[c for c in safe_cols if c in df.columns]]

    if df.empty:
        st.info("No users found.")
    else:
        st.dataframe(df, use_container_width=True)

