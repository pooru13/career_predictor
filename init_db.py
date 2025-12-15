import sqlite3

conn = sqlite3.connect("users.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    phone TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    career TEXT,
    day INTEGER,
    UNIQUE(user_id, career)
)
""")

conn.commit()
conn.close()

print("✅ Database & tables created successfully!")
