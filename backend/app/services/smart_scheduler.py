from app.database.db import get_connection

MAX_SLOTS_PER_DAY = 4


def get_available_slots(vehicle_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()

        # Prevent duplicate booking
        cursor.execute(
            """
            SELECT 1
            FROM service_bookings
            WHERE vehicle_id = ?
            LIMIT 1
            """, 
            (vehicle_id,)
        )

        if cursor.fetchone():
            return []

        # Fetch all open slots
        cursor.execute(
            """
            SELECT id, service_date, service_time
            FROM service_slots
            WHERE available = 1
            ORDER BY service_date ASC, id ASC
            """
        )
        slots = cursor.fetchall()

        # Fetch current booking load per day
        cursor.execute(
            """
            SELECT service_date, COUNT(*)
            FROM service_bookings
            GROUP BY service_date
            """
        )
        daily_load = dict(cursor.fetchall())

        available_slots = []
        for slot_id, service_date, service_time in slots:
            if daily_load.get(service_date, 0) < MAX_SLOTS_PER_DAY:
                available_slots.append({
                    "slot_id": slot_id,
                    "date": service_date,
                    "time": service_time
                })

        return available_slots

    finally:
        conn.close()