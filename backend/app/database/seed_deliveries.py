from app.database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

deliveries = [
    ("TRK001", "2026-06-15", "Chennai-Coimbatore", "Scheduled"),
    ("TRK002", "2026-06-15", "Chennai-Madurai", "Scheduled")
]

cursor.executemany("""
INSERT INTO delivery_schedule (
    vehicle_id,
    delivery_date,
    route,
    status
)
VALUES (?, ?, ?, ?)
""", deliveries)

conn.commit()
conn.close()

print("Deliveries inserted!")