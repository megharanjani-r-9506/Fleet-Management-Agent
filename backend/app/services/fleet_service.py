from app.database.db import get_connection


def find_replacement_vehicle(
    excluded_vehicle,
    delivery_date
):

    conn = get_connection()
    cursor = conn.cursor()

    # Vehicles already scheduled that day
    cursor.execute("""
        SELECT vehicle_id
        FROM delivery_schedule
        WHERE delivery_date = ?
        AND status = 'Scheduled'
    """, (delivery_date,))

    assigned = {
        row[0]
        for row in cursor.fetchall()
    }

    # Find free vehicle
    cursor.execute("""
        SELECT vehicle_id
        FROM vehicles
        WHERE vehicle_id != ?
    """, (excluded_vehicle,))

    candidates = cursor.fetchall()

    conn.close()

    for (vehicle_id,) in candidates:

        if vehicle_id not in assigned:
            return vehicle_id

    return None