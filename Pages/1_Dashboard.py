import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import csv
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

# Paths
data_folder = Path("DATA")

# Page config
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# Ensure state keys exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = None

# Guard: only logged-in users
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()

# ----------------- DOMAIN DASHBOARD -------------------

# Cyber
def cyber_dashboard():
    st.header("🔐 Cybersecurity Dashboard")

    df = pd.read_csv(data_folder / "cyber_incidents.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    st.subheader("Incident Table")
    st.dataframe(df)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # KPIs
    col1, col2 = st.columns(2)
    col1.metric("Total Incidents", len(df))
    col2.metric("Open Incidents", len(df[df["status"] == "Open"]))

    # Plots 
    st.subheader("Incident Type Breakdown") 
    fig1 = px.pie(df, names="category", title="Categories") 
    st.plotly_chart(fig1)

    phishing = df[df["category"] == "Phishing"] 
    st.subheader("Phishing Trend Over Time") 
    phishing = df[df["category"] == "Phishing"] 
    fig2 = px.line(phishing, x="timestamp", y="severity",color="category", title="Phishing Severity Trend") 
    st.plotly_chart(fig2)

# DataScience
def data_science_dashboard():
    st.header("📊 Data Science Dashboard")

    df = pd.read_csv(data_folder / "datasets_metadata.csv")

    st.subheader("Dataset Inventory")
    st.dataframe(df)

    # ------- KPIs -------
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Datasets", len(df))

    # Safe access based on your schema
    total_size = df["file_size_mb"].sum() if "file_size_mb" in df else 0
    col2.metric("Total Size (MB)", total_size)

    largest_size = df["file_size_mb"].max() if "file_size_mb" in df else 0
    col3.metric("Largest Dataset (MB)", largest_size)

    # ------- Bar Chart -------
    if "dataset_name" in df.columns and "file_size_mb" in df.columns:
        st.subheader("Dataset Size by Category")
        fig1 = px.bar(df, x="dataset_name", y="file_size_mb", color="category")
        st.plotly_chart(fig1)

    # ------- Scatter Plot (record_count vs file_size_mb) -------
    if "record_count" in df.columns and "file_size_mb" in df.columns:
        st.subheader("File Size vs Record Count")
        fig2 = px.scatter(df, x="file_size_mb", y="record_count", color="category")
        st.plotly_chart(fig2)

#IT
def it_operations_dashboard():
    st.header("🛠 IT Operations Dashboard")

    df = pd.read_csv(data_folder / "it_tickets.csv")

    st.subheader("Ticket Table")
    st.dataframe(df)

    # ------- KPIs -------
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tickets", len(df))

    # Avg resolution time (optional)
    if "resolution_time" in df:
        col2.metric("Avg Resolution (hrs)", round(df["resolution_time"].mean(), 2))
    else:
        col2.metric("Avg Resolution (hrs)", "N/A")

    # Most common category (optional)
    if "category" in df:
        col3.metric("Most Common Category", df["category"].mode()[0])
    else:
        col3.metric("Most Common Category", "N/A")

    # ------- Tickets Assigned per Staff -------
    if "assigned_to" in df:
        st.subheader("Tickets Assigned per Staff")

        y_col = "resolution_time" if "resolution_time" in df else None
        fig1 = px.bar(df, x="assigned_to", y=y_col, color="status")
        st.plotly_chart(fig1)

    # ------- Resolution Trend -------
    st.subheader("Resolution Trend")

    time_col = "timestamp" if "timestamp" in df else (
               "date_created" if "date_created" in df else None)

    if time_col and "resolution_time" in df:
        fig2 = px.line(df, x=time_col, y="resolution_time")
        st.plotly_chart(fig2)
    else:
        st.info("No timestamp or resolution_time column to show trend.")
    
# ---------------- ROLE-BASED AUTO DASHBOARD ----------------
def show_dashboard():
    role = st.session_state.get("role")

    if role == "cyber":
        cyber_dashboard()
    elif role == "datascience":
        data_science_dashboard()
    elif role == "it":
        it_operations_dashboard()
    else:
        st.info("Please select a domain above.")

show_dashboard()

# ---------------- LOGOUT BUTTON ----------------
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = None
    st.switch_page("Home.py")
