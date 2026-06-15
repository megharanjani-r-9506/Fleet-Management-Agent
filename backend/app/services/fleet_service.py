from app.database.db import get_connection


def find_replacement_vehicle(vehicle_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT v.vehicle_id
    FROM vehicles v
    WHERE v.vehicle_id != ?
    AND v.vehicle_id NOT IN (
        SELECT vehicle_id
        FROM delivery_schedule
        WHERE status = 'Scheduled'
    )
    LIMIT 1
    """, (vehicle_id,))

    vehicle = cursor.fetchone()

    conn.close()

    if vehicle:
        return vehicle[0]

    return None