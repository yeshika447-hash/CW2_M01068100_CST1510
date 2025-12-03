
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

# Theme toggle
st.subheader("Appearance")

# Initialize session state for theme
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Toggle button
if st.button("Toggle Dark / Light Mode"):
     st.session_state.dark_mode = not st.session_state.dark_mode

# Apply CSS based on theme
if st.session_state.dark_mode:
    dark_css = """
    <style>
        body, .stApp {
            background-color: #0e1117;
            color: #f0f0f0;
        }
        .stButton>button {
            background-color: #262730;
            color: #f0f0f0;
        }
        .stSidebar {
            background-color: #1e1f29;
            color: #f0f0f0;
        }
    </style>
    """
    st.markdown(dark_css, unsafe_allow_html=True)
else:
    light_css = """
    <style>
        body, .stApp {
            background-color: #ffffff;
            color: #000000;
        }
        .stButton>button {
            background-color: #e0e0e0;
            color: #000000;
        }
        .stSidebar {
            background-color: #f8f8f8;
            color: #000000;
        }
    </style>
    """
    st.markdown(light_css, unsafe_allow_html=True)