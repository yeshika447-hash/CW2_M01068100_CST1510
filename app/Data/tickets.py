import pandas as pd
from app.Data.db import connect_database
def insert_ticket(ticket_id,priority,description,status,assigned_to,created_at,resolution_time_hours):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO it_tickets
        (ticket_id,priority,description,status,assigned_to,created_at,resolution_time_hours)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (ticket_id,priority,description,status,assigned_to,created_at,resolution_time_hours))

    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()

    return ticket_id


def get_all_tickets():
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
    conn.close()
    return df
