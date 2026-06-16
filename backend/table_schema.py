from app.database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

tables = [
    "vehicles",
    "telemetry",
    "predictions",
    "maintenance_schedule",
    "service_slots",
    "service_bookings",
    "delivery_schedule"
]

for table in tables:

    print(f"\n===== {table} =====")

    cursor.execute(f"PRAGMA table_info({table})")

    for col in cursor.fetchall():
        print(col)

conn.close()