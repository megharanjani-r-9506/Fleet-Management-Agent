from app.database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT * FROM service_slots")

for row in cursor.fetchall():
    print(row)

conn.close()