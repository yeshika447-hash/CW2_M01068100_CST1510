import streamlit as st
from app.Data.users import get_all_users
from app.Services.user_service import migrate_users_from_file
from app.Data.db import connect_database
from app.Data.incidents import get_all_incidents
conn = connect_database()

st.set_page_config(page_title="Users", page_icon="👤", layout="wide")

st.title("👤 Registered Users")

df = get_all_incidents(conn)
print(f"Total incidents: {len(df)}")

df = migrate_users_from_file()
safe_cols = ["username", "role"]

df = get_all_users()
safe_cols = ["id", "username", "role"]

df = df[[col for col in safe_cols if col in df.columns]]

if df.empty:
    st.info("No users found.")
else:
    st.dataframe(df, use_container_width=True)

