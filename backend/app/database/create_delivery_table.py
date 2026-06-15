from app.database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS delivery_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id TEXT,
    delivery_date TEXT,
    route TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()

print("delivery_schedule table created!")