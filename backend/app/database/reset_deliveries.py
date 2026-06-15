from app.database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("DELETE FROM delivery_schedule")

conn.commit()
conn.close()

print("All deliveries deleted!")