import bcrypt
import sqlite3
import pandas as pd
from pathlib import Path
from app.Data.db import connect_database
from app.Data.users import get_user_by_username, insert_user
from app.Data.schema import create_users_table

DATA_DIR = Path("DATA")

def register_user(username, password, role='user'):
    """Register new user with password hashing."""
    # Hash password
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    # Insert into database
    insert_user(username, password_hash, role)
    return True, f"User '{username}' registered successfully."


def login_user(username, password):
    """Authenticate user."""
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."
    
    # Verify password
    stored_hash = user[2]  # password_hash column
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, "Login successful!"
    
    return False, "Incorrect password."


def migrate_users_from_file(filepath='DATA/users.txt'):
    """Migrate users from a text file into the database.
    
    Expected file format per line:
        username,password,role
    """
    file_path = Path(filepath)
    if not file_path.exists():
        return False, f"File not found: {filepath}"

    conn = connect_database()
    create_users_table(conn)  # ensure table exists

    migrated = 0
    skipped = 0

    with file_path.open('r') as file:
        for line in file:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            try:
                username, password, role = line.split(',')
            except ValueError:
                skipped += 1
                continue

            # Skip if user already exists
            if get_user_by_username(username):
                skipped += 1
                continue

            # Hash password
            password_hash = bcrypt.hashpw(
                password.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

            # Insert user
            insert_user(username, password_hash, role)
            migrated += 1

    return True, f"Migrated: {migrated} users | Skipped: {skipped} lines."
