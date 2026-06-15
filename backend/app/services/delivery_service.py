from app.database.db import get_connection


def has_scheduled_delivery(vehicle_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM delivery_schedule
    WHERE vehicle_id = ?
      AND status = 'Scheduled'
    """, (vehicle_id,))

    delivery = cursor.fetchone()

    conn.close()

    return delivery is not None