import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "fleet.db"

def clear_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tables = [
        "predictions",
        "maintenance_schedule",
        "service_bookings",
        "delivery_schedule",
        "telemetry"
    ]

    for table in tables:
        try:
            cursor.execute(f"DELETE FROM {table}")
            print(f"Cleared table: {table}")
        except Exception as e:
            print(f"Skipping {table}: {e}")

    conn.commit()
    conn.close()
    print("\n✅ All possible tables cleared successfully!")

if __name__ == "__main__":
    clear_tables()