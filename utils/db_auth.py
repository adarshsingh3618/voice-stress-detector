import sqlite3
import bcrypt

DB_NAME = "users.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    # Stress history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stress_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        time TEXT,
        voice_score REAL,
        text_score REAL,
        final_score REAL
    )
    """)

    conn.commit()
    conn.close()


# ---------------- AUTH ---------------- #

def signup_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        return False, "User already exists"

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed)
    )

    conn.commit()
    conn.close()

    return True, "Signup successful"


def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()

    conn.close()

    if result and bcrypt.checkpw(password.encode(), result[0]):
        return True, "Login successful"

    return False, "Invalid credentials"


# ---------------- HISTORY ---------------- #

def save_stress(username, time, voice, text, final):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO stress_history (username, time, voice_score, text_score, final_score)
    VALUES (?, ?, ?, ?, ?)
    """, (username, time, voice, text, final))

    conn.commit()
    conn.close()


def load_stress(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT time, voice_score, text_score, final_score
    FROM stress_history
    WHERE username=?
    ORDER BY id ASC
    """, (username,))

    data = cursor.fetchall()
    conn.close()

    history = []
    for row in data:
        history.append({
            "time": row[0],
            "voice_score": row[1],
            "text_score": row[2],
            "final_score": row[3]
        })

    return history