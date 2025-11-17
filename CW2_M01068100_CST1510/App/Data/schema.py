#WEEK 8
import sqlite3

def create_users_table(conn):
    """Create users table"""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
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
    conn.commit()


def create_datasets_metadata_table(conn):
    """Create datasets_metadata table."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT NOT NULL,
            source TEXT,
            created_on TEXT,
            last_updated TEXT,
            description TEXT
        )
    """)
    conn.commit()


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
    conn.commit()


def create_all_tables(conn):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
