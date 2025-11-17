import bcrypt
import sqlite3
import pandas as pd
from pathlib import Path
from CW2_M01068100_CST1510.app.Data.db import connect_database
from CW2_M01068100_CST1510.app.Data.users import get_user_by_username, insert_user
from CW2_M01068100_CST1510.app.Data.schema import create_users_table

DATA_DIR = Path("DATA")

def load_csv_to_table(csv_path, table_name, conn):
    """
    Load CSV data into a table using pandas.

    Args:
        csv_path: Path to CSV file
        table_name: Name of database table
        conn: SQLite connection
    """

    df = pd.read_csv(csv_path)

    df.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False
    )

    print(f"📥 Loaded {len(df)} rows into '{table_name}' from {csv_path.name}")


def load_all_csv_data(conn):
    conn = connect_database()
    total = 0
    total += load_csv_to_table
    load_csv_to_table(DATA_DIR / "cyber_incidents.csv", "cyber_incidents", conn)
    load_csv_to_table(DATA_DIR / "datasets_metadata.csv", "datasets_metadata", conn)
    load_csv_to_table(DATA_DIR / "it_tickets.csv", "it_tickets", conn)

    return total
    conn.close()
