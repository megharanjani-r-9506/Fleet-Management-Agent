from app.database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT * FROM vehicles")

for row in cursor.fetchall():
    print(row)

conn.close()