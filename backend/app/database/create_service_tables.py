from app.database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

# Service Slots
cursor.execute("""
CREATE TABLE IF NOT EXISTS service_slots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_date TEXT,
    service_time TEXT,
    available INTEGER
)
""")

# Bookings
cursor.execute("""
CREATE TABLE IF NOT EXISTS service_bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id TEXT,
    service_date TEXT,
    service_time TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()

print("Service portal tables created!")