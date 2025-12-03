import streamlit as st

st.set_page_config(page_title="Multi-domain Platform", page_icon="🎓", layout="wide")

st.title("Multi-domain Intelligence Platform")

st.write("Welcome! Click below to continue.")

if st.button("Go to Login Page"):
    st.switch_page("pages/login.py")
