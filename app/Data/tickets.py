import pandas as pd
from app.Data.db import connect_database

def insert_ticket(date, issue_type, severity, status, assigned_to, description):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO it_tickets
        (date, issue_type, severity, status, assigned_to, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, issue_type, severity, status, assigned_to, description))

    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()

    return ticket_id


def get_all_tickets():
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM it_tickets", conn)
    conn.close()
    return df
