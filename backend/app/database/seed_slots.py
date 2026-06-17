from datetime import datetime, timedelta
from app.database.db import get_connection

SLOT_TIMES = [
    "09:00 AM",
    "10:00 AM",
    "11:00 AM",
    "02:00 PM",
]

DAYS_AHEAD = 10


def seed_slots():

    conn = get_connection()
    cursor = conn.cursor()

    today = datetime.now().date()

    for i in range(DAYS_AHEAD):

        target_date = today + timedelta(days=i)

        for time in SLOT_TIMES:

            # prevent duplicates (VERY IMPORTANT)
            cursor.execute("""
                SELECT 1 FROM service_slots
                WHERE service_date = ? AND service_time = ?
            """, (str(target_date), time))

            if cursor.fetchone():
                continue

            cursor.execute("""
                INSERT INTO service_slots (service_date, service_time, available)
                VALUES (?, ?, 1)
            """, (str(target_date), time))

    conn.commit()
    conn.close()

    print("10-day service slots seeded successfully")


if __name__ == "__main__":
    seed_slots()