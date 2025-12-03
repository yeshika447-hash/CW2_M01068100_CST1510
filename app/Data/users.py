from app.Data.db import connect_database
import bcrypt
import pandas as pd

def get_user_by_username(username: str, conn = None):
    """Retrieve user by username."""
    own_conn = False
    if conn is None:
        conn = connect_database()
        own_conn = True
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if own_conn:
        conn.close()
    return user

def insert_user(conn, username, plain_text_password, password_hash, role):
    
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    password_hash = hashed.decode('utf-8')

    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    conn.close()

def update_user(user_id, new_username=None, new_password=None, new_role=None):
    """
    Update user fields (username, password, role).
    Only updates fields that are provided.
    """

    conn = connect_database()
    cursor = conn.cursor()

    updates = []
    params = []

    # Update username
    if new_username:
        updates.append("username = ?")
        params.append(new_username)

    # Update password
    if new_password:
        password_bytes = new_password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

        updates.append("password_hash = ?")
        params.append(hashed)

    # Update role
    if new_role:
        updates.append("role = ?")
        params.append(new_role)

    if not updates:
        conn.close()
        return 0  # nothing to update

    query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
    params.append(user_id)

    cursor.execute(query, params)
    conn.commit()

    affected = cursor.rowcount
    conn.close()
    return affected

def delete_user(user_id):
    """Delete a user permanently."""
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()

    deleted = cursor.rowcount
    conn.close()

    return deleted

def get_all_users():
    """Return all users as a pandas DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM users ORDER BY id DESC", conn)
    conn.close()
    return df
