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

# Cyber Analytics
def cyber_analytics():
    st.header("🔐 Cybersecurity Analytics")

    df = pd.read_csv(data_folder / "cyber_incidents.csv")

    st.subheader("Phishing Spike Detection")
    phishing = df[df["incident_type"] == "Phishing"]
    phishing_trend = phishing.groupby("date").size().reset_index(name="count")

    fig = px.line(phishing_trend, x="date", y="count", title="Phishing Trend Over Time")
    st.plotly_chart(fig)

    st.subheader("Longest Resolution Time by Category")
    resolution = df.groupby("incident_type")[["resolution_time"]].mean().reset_index()
    fig2 = px.bar(resolution, x="incident_type", y="resolution_time", title="Incident Type Resolution Time")
    st.plotly_chart(fig2)

# Datascience Analytics
def datascience_analytics():
    st.header("📊 Data Science Analytics")

    df = pd.read_csv(data_folder / "datasets_metadata.csv")

    st.subheader("Dataset Size Distribution")
    fig1 = px.histogram(df, x="size_mb", title="Dataset Size Distribution")
    st.plotly_chart(fig1)

    st.subheader("Stale Datasets (Not Updated in 90+ Days)")
    df["last_updated"] = pd.to_datetime(df["last_updated"])
    stale = df[df["last_updated"] < pd.Timestamp.now() - pd.Timedelta(days=90)]
    st.dataframe(stale)

# IT Analytics

def it_analytics():
    st.header("🛠 IT Operations Analytics")

    df = pd.read_csv(data_folder / "it_tickets.csv")

    st.subheader("Staff Resolution Performance")
    performance = df.groupby("assigned_to")[["resolution_time"]].mean().reset_index()
    fig = px.bar(performance, x="assigned_to", y="resolution_time", title="Avg Resolution Time per Staff")
    st.plotly_chart(fig)

    st.subheader("Status Bottleneck Detection")
    bottleneck = df.groupby("status").size().reset_index(name="count")
    fig2 = px.bar(bottleneck, x="status", y="count", title="Ticket Count by Status")
    st.plotly_chart(fig2)

# MAIN
if role == "cyber":
    cyber_analytics()
elif role == "datascience":
    datascience_analytics()
elif role == "it":
    it_analytics()
else:
    st.warning("No role detected.")