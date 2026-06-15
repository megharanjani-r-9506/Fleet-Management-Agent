from app.database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
SELECT * FROM telemetry
ORDER BY id DESC
LIMIT 10
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()