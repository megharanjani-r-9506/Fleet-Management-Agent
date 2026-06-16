from app.database.db import get_connection

def maintenance_exists(vehicle_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 FROM maintenance_schedule
        WHERE vehicle_id = ?
        AND status = 'Pending'
    """, (vehicle_id,))

    result = cursor.fetchone()
    conn.close()

    return result is not None