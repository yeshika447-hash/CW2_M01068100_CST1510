import pandas as pd
from app.Data.db import connect_database

def insert_incident(conn, date_reported, incident_type, severity, status, description, reported_by=None):
    def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):"""
    Insert a new cyber incident into the database.
    
    Args:
        conn: Database connection
        date: Incident date (YYYY-MM-DD)
        incident_type: Type of incident
        severity: Severity level
        status: Current status
        description: Incident description
        reported_by: Username of reporter (optional)
        
    Returns:
        int: ID of the inserted incident
    """
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cyber_incidents 
        (date_reported, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date_reported, incident_type, severity, status, description, reported_by))
    conn.commit()
    incident_id = cursor.lastrowid
    conn.close()
    return incident_id

def get_all_incidents():
    def get_all_incidents(conn):"""
    Retrieve all incidents from the database.
    
    Returns:
        pandas.DataFrame: All incidents
    """
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

def update_incident_status(conn, incident_id, new_status):
    """
    Update the status of an incident.
    Returns number of modified rows (0 or 1).
    """
    cursor = conn.cursor()

    query = """
        UPDATE cyber_incidents
        SET status = ?
        WHERE id = ?
    """

    cursor.execute(query, (new_status, incident_id))
    conn.commit()

    return cursor.rowcount


def delete_incident(conn, incident_id):
    """
    Delete an incident from the database.
    WARNING: DELETE is permanent.
    """
    cursor = conn.cursor()

    query = "DELETE FROM cyber_incidents WHERE id = ?"

    cursor.execute(query, (incident_id,))
    conn.commit()

    return cursor.rowcount

def get_incidents_by_type_count(conn):
    """
    Count incidents by type.
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)


def get_high_severity_by_status(conn):
    """
    Count high severity incidents grouped by status.
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)


def get_incident_types_with_many_cases(conn, min_count=5):
    """
    Find incident types with more than min_count cases.
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn, params=(min_count,))