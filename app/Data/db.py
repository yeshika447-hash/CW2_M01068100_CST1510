#WEEK 8

import sqlite3
from pathlib import Path

DATA_DIR = Path("DATA")
DB_PATH =Path("DATA") / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    print(f"Connected to database at: {db_path}")
    return conn

from schema import (
    create_users_table,
    create_cyber_incidents_table,
    create_datasets_metadata_table,
    create_it_tickets_table
)
from Services.user_service import migrate_users_from_file
from load import load_all_csv_data


def create_all_tables(conn):
    """
    Create all database tables.
    """
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
    print(" All tables created successfully!")


def setup_database_complete():
    """
    Complete database setup:
    1. Connect to database
    2. Create all tables
    3. Migrate users from users.txt
    4. Load CSV data for all domains
    5. Verify setup
    """

    print("\n" + "="*60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("="*60)

    # Step 1: Connect
    print("\n[1/5] Connecting to database...")
    conn = connect_database()
    print("       Connected")

    # Step 2: Create tables
    print("\n[2/5] Creating database tables...")
    create_all_tables(conn)

    # Step 3: Migrate users
    print("\n[3/5] Migrating users from users.txt...")
    migrated_count = migrate_users_from_file(conn)
    print(f"       Migrated {migrated_count} users")

    # Step 4: Load CSV data
    print("\n[4/5] Loading CSV data...")
    total_rows = load_all_csv_data(conn)
    print(f"       Loaded {total_rows} rows")

    # Step 5: Verify
    print("\n[5/5] Verifying database setup...")
    cursor = conn.cursor()

    tables = ["users", "cyber_incidents", "datasets_metadata", "it_tickets"]

    print("\n Database Summary:")
    print(f"{'Table':<25} {'Row Count':<15}")
    print("-" * 40)

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<15}")

    conn.close()

    print("\n" + "="*60)
    print(" DATABASE SETUP COMPLETE!")
    print("="*60)
    print(f"\n Database location: {DB_PATH.resolve()}")
    print("\nYou're ready for Week 9 (Streamlit web interface)!")