import sqlite3
import bcrypt
import streamlit as st

DB_NAME = "database.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# -----------------------
# CREATE ACCOUNT
# -----------------------
def register(username, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    # Check if username or email already exists
    cursor.execute(
        "SELECT * FROM users WHERE username=? OR email=?",
        (username, email)
    )

    if cursor.fetchone():
        conn.close()
        return False

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    cursor.execute(
        """
        INSERT INTO users(username,email,password)
        VALUES(?,?,?)
        """,
        (username, email, hashed)
    )

    conn.commit()
    conn.close()

    return True


# -----------------------
# LOGIN
# -----------------------
def login(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        stored_password = user[3]

        if bcrypt.checkpw(
            password.encode(),
            stored_password
        ):
            return user

    return None


# -----------------------
# LOGOUT
# -----------------------
def logout():

    st.session_state.logged_in = False
    st.session_state.user = None