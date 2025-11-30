import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title = "Intelligence Platform",

    layout = "wide"
)

st.title("📊Dashboard")
st.write("Welcome to Streamlit!")

from app.Data.db import connect_database

from app.Data.users import (
    get_user_by_username, 
    insert_user
    )

from app.Data.incidents import (
    get_all_incidents, 
    insert_incident, 
    update_incident_status, 
    delete_incident)

from app.Data.datasets import get_all_datasets

from app.Data.tickets import get_all_tickets

conn = connect_database()

incidents = get_all_incidents(conn)

st.dataframe(incidents, use_container_width=True)