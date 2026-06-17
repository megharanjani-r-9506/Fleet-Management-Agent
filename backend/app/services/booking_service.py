from app.database.db import get_connection


def create_booking(
    vehicle_id,
    slot_id,
    service_date,
    service_time
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO service_bookings (
            vehicle_id,
            service_date,
            service_time,
            status
        )
        VALUES (?, ?, ?, ?)
    """, (
        vehicle_id,
        service_date,
        service_time,
        "Booked"
    ))

    cursor.execute("""
        UPDATE service_slots
        SET available = 0
        WHERE id = ?
    """, (slot_id,))

    conn.commit()
    conn.close()

    return {
        "service_date": service_date,
        "service_time": service_time
    }