
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

st.title("⚙️ Settings")
st.write("User configuration settings here.")

