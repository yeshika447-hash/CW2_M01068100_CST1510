import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
from app.Data.db import connect_database
import csv

DB_PATH =Path("DATA") / "intelligence_platform.db"
data_folder = Path("DATA")

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# Ensure state keys exist (in case user opens this page first)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Guard: if not logged in, send user back
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")   # back to the first page
    st.stop()

# If logged in, show dashboard content
st.title("📊 Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")

# dashboard layout
def cyber_dashboard():
    st.header("🔐 Cybersecurity Dashboard")

    #load cyber incidents
    df = pd.read_csv(data_folder / "cyber_incidents.csv")
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

def data_science_dashboard():
    st.header("📊 Data Science Dashboard")

    df = pd.read_csv(data_folder / "datasets_metadata.csv")
    st.subheader("Dataset Inventory")
    st.dataframe(df)

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Datasets", len(df))
    col2.metric("Total Size (MB)", df["size_mb"].sum())
    col3.metric("Largest Dataset (MB)", df["size_mb"].max())

    # Dataset size bar chart
    st.subheader("Dataset Size by Department")
    fig1 = px.bar(df, x="dataset_name", y="size_mb", color="owner")
    st.plotly_chart(fig1)

    # Size vs Rows scatter
    st.subheader("Size vs Rows")
    fig2 = px.scatter(df, x="size_mb", y="num_rows", color="owner")
    st.plotly_chart(fig2)

def it_operations_dashboard():
    st.header("🛠 IT Operations Dashboard")

    df = pd.read_csv(data_folder / "it_tickets.csv")
    st.subheader("Ticket Table")
    st.dataframe(df)

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tickets", len(df))
    col2.metric("Avg Resolution (hrs)", round(df["resolution_time"].mean(), 2))
    col3.metric("Most Common Category", df["category"].mode()[0])

    # Tickets per staff
    st.subheader("Tickets Assigned per Staff")
    fig1 = px.bar(df, x="assigned_to", y="resolution_time", color="status")
    st.plotly_chart(fig1)

    # Resolution trend
    st.subheader("Resolution Time Trend")
    fig2 = px.line(df, x="date", y="resolution_time", title="Resolution Trend")
    st.plotly_chart(fig2)

    # Sidebar filters
with st.sidebar:
    st.header("Filters")
    n_points = st.slider("Number of data points", 10, 200, 50)

def show_dashboard():
    role = st.session_state.get("role", None)
    if role == "cyber":
        cyber_dashboard()
    elif role == "datascience":
        data_science_dashboard()
    elif role == "it":
        it_operations_dashboard()
    else:
        st.warning("No role assigned or user not logged in.")

role = st.session_state.get("role", None)
def load_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))
    
    if role == "cyber":
        df = load_csv(data_folder / "cyber_incidents.csv")

        st.subheader("Incident Severity Trend")
        fig = px.line(df, x="date", y="severity", color="incident_type",
                    title="Severity over Time")
        st.plotly_chart(fig)

        st.subheader("Incident Counts by Type")
        counts = {}
        for row in df:
            itype = row["incident_type"]
            counts[itype] = counts.get(itype, 0) + 1

        count_rows = [{"incident_type": k, "count": v} for k, v in counts.items()]
        fig2 = px.bar(count_rows, x="incident_type", y="count",
                    title="Incident Counts")
        st.plotly_chart(fig2)

        with st.expander("See raw data"):
            st.write(df)

    elif role == "datascience":
        df = load_csv(data_folder / "datasets_metadata.csv")

        st.subheader("Dataset Sizes by Owner")
        fig = px.bar(df, x="dataset_name", y="size_mb", color="owner",
                    title="Dataset Sizes")
        st.plotly_chart(fig)

        st.subheader("Rows vs Size Scatter")
        fig2 = px.scatter(df, x="num_rows", y="size_mb", color="owner",
                        title="Rows vs Size")
        st.plotly_chart(fig2)

        with st.expander("See raw data"):
            st.write(df)

    elif role == "it":
        df = load_csv(data_folder / "it_tickets.csv")

        st.subheader("Tickets Resolution Trend")
        fig = px.line(df, x="date", y="resolution_time", color="status",
                    title="Resolution Time Trend")
        st.plotly_chart(fig)

        st.subheader("Tickets per Staff")
        staff_counts = {}
        for row in df:
            staff = row["assigned_to"]
            staff_counts[staff] = staff_counts.get(staff, 0) + 1

        staff_rows = [{"staff": k, "tickets": v} for k, v in staff_counts.items()]
        fig2 = px.bar(staff_rows, x="staff", y="tickets",
                    title="Tickets per Staff")
        st.plotly_chart(fig2)

        with st.expander("See raw data"):
            st.write(df)

# Logout button
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.switch_page("Home.py")


show_dashboard()