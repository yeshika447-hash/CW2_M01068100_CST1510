import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

data_folder = Path("DATA")

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to access Analytics.")
    st.stop()

st.title("📊 Domain Analytics Center")
role = st.session_state.get("role", None)

# ---------------- CYBER ANALYTICS -------------------
def cyber_analytics():
    st.header("🔐 Cybersecurity Analytics")

    df = pd.read_csv(data_folder / "cyber_incidents.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # --- Trend of incidents over time ---
    st.subheader("Incident Trend Over Time")
    trend = df.groupby(df["timestamp"].dt.date).size().reset_index(name="count")
    fig = px.line(trend, x="timestamp", y="count", title="Daily Incident Trend")
    st.plotly_chart(fig)

    # --- Count per category ---
    st.subheader("Incidents by Category")
    fig2 = px.bar(df.groupby("category").size().reset_index(name="count"),
                  x="category", y="count", title="Incident Count per Category")
    st.plotly_chart(fig2)

    # --- Severity distribution ---
    st.subheader("Severity Distribution")
    fig3 = px.pie(df, names="severity", title="Incident Severity Breakdown")
    st.plotly_chart(fig3)


# ---------------- DATA SCIENCE ANALYTICS -------------------
def datascience_analytics():
    st.header("📊 Data Science Analytics")

    df = pd.read_csv(data_folder / "datasets_metadata.csv")
    df["upload_date"] = pd.to_datetime(df["upload_date"])

    # --- Dataset size (rows × columns) ---
    st.subheader("Dataset Size Distribution (Rows × Columns)")
    df["size"] = df["rows"] * df["columns"]
    fig1 = px.histogram(df, x="size", title="Dataset Size Distribution")
    st.plotly_chart(fig1)

    # --- Recently uploaded datasets ---
    st.subheader("Recently Uploaded Datasets (Last 30 Days)")
    recent = df[df["upload_date"] >= pd.Timestamp.now() - pd.Timedelta(days=30)]
    st.dataframe(recent)

    # --- Uploaders ranking ---
    st.subheader("Top Dataset Uploaders")
    uploader_count = df.groupby("uploaded_by").size().reset_index(name="count")
    fig2 = px.bar(uploader_count, x="uploaded_by", y="count",
                  title="Datasets Uploaded per User")
    st.plotly_chart(fig2)


# ---------------- IT OPERATIONS ANALYTICS -------------------
def it_analytics():
    st.header("🛠 IT Operations Analytics")

    df = pd.read_csv(data_folder / "it_tickets.csv")
    df["created_at"] = pd.to_datetime(df["created_at"])

    # --- Average resolution time per staff ---
    st.subheader("Avg Resolution Time Per Staff")
    perf = df.groupby("assigned_to")[["resolution_time_hours"]].mean().reset_index()
    fig = px.bar(perf, x="assigned_to", y="resolution_time_hours",
                 title="Average Resolution Time (Hours)")
    st.plotly_chart(fig)

    # --- Tickets by status ---
    st.subheader("Ticket Status Overview")
    status_count = df.groupby("status").size().reset_index(name="count")
    fig2 = px.bar(status_count, x="status", y="count", title="Ticket Count by Status")
    st.plotly_chart(fig2)

    # --- Ticket trend over time ---
    st.subheader("Ticket Volume Over Time")
    trend = df.groupby(df["created_at"].dt.date).size().reset_index(name="count")
    fig3 = px.line(trend, x="created_at", y="count", title="Daily Ticket Trend")
    st.plotly_chart(fig3)


# -------- MAIN ROLE SWITCH ----------
if role == "cyber":
    cyber_analytics()
elif role == "datascience":
    datascience_analytics()
elif role == "it":
    it_analytics()
else:
    st.warning("No role detected.")
