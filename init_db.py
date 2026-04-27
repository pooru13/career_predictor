import sqlite3

conn = sqlite3.connect("users.db")
cur = conn.cursor()

# USERS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    phone TEXT
)
""")

# PROGRESS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS progress (
    user_id INTEGER,
    career TEXT,
    day INTEGER,
    PRIMARY KEY (user_id, career)
)
""")

# ✅ IMPORTANT → CAREER HISTORY TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS career_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    career TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully!")