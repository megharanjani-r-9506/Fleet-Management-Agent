from app.database.db import get_connection


def has_upcoming_delivery(vehicle_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, delivery_date, route
        FROM delivery_schedule
        WHERE vehicle_id = ?
        AND status = 'Scheduled'
        LIMIT 1
    """, (vehicle_id,))

    delivery = cursor.fetchone()

    conn.close()

    return delivery

def reassign_delivery(
    vehicle_id,
    replacement_vehicle
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE delivery_schedule
        SET vehicle_id = ?
        WHERE vehicle_id = ?
        AND status = 'Scheduled'
    """, (
        replacement_vehicle,
        vehicle_id
    ))

    conn.commit()
    conn.close()