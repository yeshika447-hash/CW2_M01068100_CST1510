from db import connect_database

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

def insert_user(username, password_hash, role='user', conn = None):
    """Insert new user."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role)
    )
    conn.commit()
    conn.close()