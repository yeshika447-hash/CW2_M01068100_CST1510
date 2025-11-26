#WEEK 8
import sqlite3
import pandas as pd
from app.Data.db import connect_database

def create_users_table(conn):
    """Create users table"""
    cursor = conn.cursor()
    cursor.execute("""
        (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT NOT NULL UNIQUE,
                   password_hash TEXT NOT NULL,
                   role TEXT DEFAULT 'user'
        )
    """)
    conn.commit()

def create_cyber_incidents_table(conn):
    """Create cyber_incidents table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_type TEXT NOT NULL,
            description TEXT,
            reported_by INTEGER,
            date_reported TEXT,
            status TEXT DEFAULT 'Open',
            FOREIGN KEY (reported_by) REFERENCES users(id)
        )
    """)
    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        incident_type TEXT,
        severity TEXT,
        status TEXT,
        description TEXT,
        reported_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (reported_by) REFERENCES users(username)
    )
    """
    cursor.execute(create_table_sql)
    conn.commit()
    print("✅ cyber_incidents table created successfully!")

    conn.commit()


def create_datasets_metadata_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    Create the datasets_metadata table.

    Required columns:
    - id INTEGER PRIMARY KEY AUTOINCREMENT
    - dataset_name TEXT NOT NULL
    - category TEXT
    - source TEXT
    - last_updated TEXT
    - record_count INTEGER
    - file_size_mb REAL
    - created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_name TEXT NOT NULL,
        category TEXT,
        source TEXT,
        last_updated TEXT,
        record_count INTEGER,
        file_size_mb REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    cursor.execute(create_table_sql)
    conn.commit()
    print(" datasets_metadata table created successfully!")


def create_it_tickets_table(conn):
    """Create it_tickets table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            issue_title TEXT NOT NULL,
            issue_description TEXT,
            priority TEXT DEFAULT 'Medium',
            status TEXT DEFAULT 'Open',
            date_created TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT UNIQUE NOT NULL,
        priority TEXT,
        status TEXT,
        category TEXT,
        subject TEXT NOT NULL,
        description TEXT,
        created_date TEXT,
        resolved_date TEXT,
        assigned_to TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    cursor.execute(create_table_sql)
    conn.commit()
    print(" it_tickets table created successfully!")
    conn.commit()

def insert_dataset(dataset_name, file_name, records, description, owner):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO datasets_metadata 
        (dataset_name, file_name, records, description, owner)
        VALUES (?, ?, ?, ?, ?)
    """, (dataset_name, file_name, records, description, owner))

    conn.commit()
    dataset_id = cursor.lastrowid
    conn.close()

    return dataset_id


def get_all_datasets():
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    conn.close()
    return df


def create_all_tables(conn):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)