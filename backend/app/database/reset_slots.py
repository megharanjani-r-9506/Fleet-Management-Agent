from app.database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("DELETE FROM service_slots")

slots = [
    ("2026-06-15", "10:00 AM", 1),
    ("2026-06-15", "02:00 PM", 1),
    ("2026-06-16", "11:00 AM", 1),
    ("2026-06-17", "09:00 AM", 1)
]

cursor.executemany("""
INSERT INTO service_slots (
    service_date,
    service_time,
    available
)
VALUES (?, ?, ?)
""", slots)

conn.commit()
conn.close()

print("Service slots reset!")