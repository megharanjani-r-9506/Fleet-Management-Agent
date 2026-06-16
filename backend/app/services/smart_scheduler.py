from app.database.db import get_connection

MAX_SLOTS_PER_DAY = 4


def select_best_slot(vehicle_id):

    conn = get_connection()
    cursor = conn.cursor()

    # prevent duplicate booking
    cursor.execute("""
        SELECT 1 FROM service_bookings
        WHERE vehicle_id = ?
        LIMIT 1
    """, (vehicle_id,))

    if cursor.fetchone():
        conn.close()
        return None

    # get slots (date + time REQUIRED)
    cursor.execute("""
        SELECT id, service_date, service_time
        FROM service_slots
        WHERE available = 1
        ORDER BY service_date ASC, id ASC
    """)

    slots = cursor.fetchall()

    if not slots:
        conn.close()
        return None

    # FIX: proper load calculation (date-only grouping is fine)
    cursor.execute("""
        SELECT service_date, COUNT(*)
        FROM service_bookings
        GROUP BY service_date
    """)

    daily_load = dict(cursor.fetchall())

    # choose slot safely
    for slot_id, date, time in slots:

        if daily_load.get(date, 0) < MAX_SLOTS_PER_DAY:
            conn.close()
            return slot_id, date, time

    conn.close()
    return None