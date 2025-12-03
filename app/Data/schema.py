#WEEK 8
from app.Data.db import connect_database

def create_users_table(conn):
    """Create users table"""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT NOT NULL UNIQUE,
                   password_hash TEXT NOT NULL,
                   role TEXT DEFAULT 'users'
        )
    """)
    conn.commit()
    
def create_cyber_incidents_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_id TEXT,
        severity TEXT,
        category TEXT,
        status TEXT,
        description TEXT,
        reported_by TEXT,
        date_reported TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (reported_by) REFERENCES users(username)
    )
    """)
    conn.commit()
    print("✅ cyber_incidents table created successfully!")


def create_datasets_metadata_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_id TEXT NOT NULL,
        name TEXT,
        num_columns INTEGER,
        num_rows INTEGER,
        uploaded_by, 
        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    print(" datasets_metadata table created successfully!")


def create_it_tickets_table(conn):
    """Create it_tickets table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            ticket_id TEXT UNIQUE NOT NULL,
            priority TEXT DEFAULT 'Medium',
            description TEXT,
            status TEXT DEFAULT 'Open',
            assigned_to TEXT,
            created_at TEXT,
            resolution_time_hours TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
    
    conn.commit()
    print(" it_tickets table created successfully!")

def create_all_tables(conn):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)