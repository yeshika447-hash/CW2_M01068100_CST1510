import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

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

st.title("📊 Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")

# ---------------- DASHBOARD FUNCTIONS ----------------
def cyber_dashboard():
    st.header("🔐 Cybersecurity Dashboard")

    df = pd.read_csv(data_folder / "cyber_incidents.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    st.subheader("Incident Table")
    st.dataframe(df)

    # KPIs
    col1, col2 = st.columns(2)
    col1.metric("Total Incidents", len(df))
    col2.metric("Open Incidents", len(df[df["status"] == "Open"]))

    # Pie chart of categories
    st.subheader("Incident Type Breakdown")
    fig1 = px.pie(df, names="category", title="Categories")
    st.plotly_chart(fig1)

    # Phishing trend
    phishing = df[df["category"] == "Phishing"]
    if not phishing.empty:
        st.subheader("Phishing Trend Over Time")
        fig2 = px.line(phishing, x="timestamp", y="severity", color="category", title="Phishing Severity Trend")
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
    fig2 = px.line(df, x="timestamp" if "timestamp" in df.columns else "date", y="resolution_time", title="Resolution Trend")
    st.plotly_chart(fig2)

# ---------------- SHOW DASHBOARD ----------------
def show_dashboard():
    role = st.session_state.get("role", "").lower()  # normalize to lowercase
    if role == "cyber":
        cyber_dashboard()
    elif role == "datascience":
        data_science_dashboard()
    elif role == "it":
        it_operations_dashboard()
    else:
        st.warning("No role assigned or user not logged in.")

# ---------------- LOGOUT BUTTON ----------------
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = None
    st.info("You have been logged out.")
    st.switch_page("Home.py")

# Run dashboard
show_dashboard()