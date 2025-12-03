import bcrypt
from pathlib import Path
from app.Data.db import connect_database
from app.Data.users import get_user_by_username, insert_user
from app.Data.schema import create_users_table


def register_user(username, password, role='user'):
    """Register a new user."""
    conn = connect_database()
    cursor = conn.cursor()

    # Check if user exists
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False, f"Username '{username}' already exists."

    # Hash password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Insert user
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, hashed, role)
    )
    conn.commit()
    conn.close()

    return True, f"User '{username}' registered successfully."


def login_user(username, password):
    """Authenticate user login."""
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."

    stored_hash = user[2]  # password_hash column

    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, "Login successful!"
    return False, "Incorrect password."


def migrate_users_from_file(filepath='DATA/users.txt'):
    """
    Migrate users from a text file.
    Expected format per line:
        username,password,role
    """
    file_path = Path(filepath)
    if not file_path.exists():
        return False, f"File not found: {filepath}"

    conn = connect_database()
    create_users_table(conn)

    migrated = 0
    skipped = 0

    with file_path.open('r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(',')
            if len(parts) != 3:
                skipped += 1
                continue

            username, password, role = parts

            # Skip existing users
            if get_user_by_username(username):
                skipped += 1
                continue

            # Hash the password
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Insert into DB
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, hashed, role)
            )
            conn.commit()

            migrated += 1

    conn.close()
    return True, f"Migrated: {migrated} users | Skipped: {skipped} lines."
