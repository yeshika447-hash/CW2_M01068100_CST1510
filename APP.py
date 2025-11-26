import streamlit as st

st.title("Hello!")
st.write("This is my first app!")

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

from app.Data.schema import get_all_datasets

from app.Data.tickets import get_all_tickets

conn = connect_database("DATA") / "intelligence_platform.db"

incidents = get_all_incidents(conn)

st.dataframe(incidents, use_container_width=True)