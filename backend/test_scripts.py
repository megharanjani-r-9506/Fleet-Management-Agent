from app.database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
    DELETE FROM maintenance_schedule
    WHERE status = 'Pending'
""")

deleted_count = cursor.rowcount

conn.commit()
conn.close()

print("=" * 50)
print(f"Deleted {deleted_count} pending maintenance records")
print("=" * 50)