from app.database.db import get_connection

def check_maintenance_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM maintenance_schedule")
    rows = cursor.fetchall()

    print("\n--- MAINTENANCE SCHEDULE DATA ---")
    print("COUNT:", len(rows))
    print()

    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    check_maintenance_table()