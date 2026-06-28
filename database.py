import sqlite3

# Connect to database
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT
)
""")

# History table
cursor.execute("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    gpa REAL,
    cgpa REAL,
    total_cu INTEGER,
    total_qp REAL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


# ---------------- USERS ---------------- #

def create_user(username, email, password):
    try:
        cursor.execute(
            "INSERT INTO users(username,email,password) VALUES(?,?,?)",
            (username, email, password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def login_user(username, password):
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )
    return cursor.fetchone()


# ---------------- HISTORY ---------------- #

def save_history(username, gpa, cgpa, total_cu, total_qp):
    cursor.execute(
        """
        INSERT INTO history
        (username,gpa,cgpa,total_cu,total_qp)
        VALUES(?,?,?,?,?)
        """,
        (
            username,
            gpa,
            cgpa,
            total_cu,
            total_qp
        )
    )
    conn.commit()
