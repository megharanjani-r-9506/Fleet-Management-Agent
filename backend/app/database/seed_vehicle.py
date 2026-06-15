from app.database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

vehicles = [
    ("TRK001", "Active"),
    ("TRK002", "Active"),
    ("TRK003", "Active"),
    ("TRK004", "Active"),
    ("TRK005", "Active")
]

cursor.executemany("""
INSERT INTO vehicles (
    vehicle_id,
    status
)
VALUES (?, ?)
""", vehicles)

conn.commit()
conn.close()

print("Vehicles inserted!")