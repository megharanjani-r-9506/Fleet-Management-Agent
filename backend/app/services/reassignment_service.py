from app.database.db import get_connection


def reassign_delivery(
    old_vehicle,
    new_vehicle
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE delivery_schedule
    SET vehicle_id = ?
    WHERE vehicle_id = ?
      AND status = 'Scheduled'
    """, (
        new_vehicle,
        old_vehicle
    ))

    conn.commit()

    rows_updated = cursor.rowcount

    conn.close()

    return rows_updated