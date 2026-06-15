from app.database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT * FROM vehicles")

vehicles = cursor.fetchall()

for vehicle in vehicles:
    print(vehicle)

conn.close()