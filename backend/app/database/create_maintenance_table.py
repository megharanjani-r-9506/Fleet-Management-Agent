import sqlite3

conn = sqlite3.connect("fleet.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS maintenance_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id TEXT,
    risk_level TEXT,
    recommendation TEXT,
    priority TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()

print("Maintenance table created.")