from app.database.db import get_connection


def create_booking(vehicle_id):

    conn = get_connection()
    cursor = conn.cursor()

    # Find first available slot
    cursor.execute("""
    SELECT id, service_date, service_time
    FROM service_slots
    WHERE available = 1
    ORDER BY id
    LIMIT 1
    """)

    slot = cursor.fetchone()

    if not slot:
        conn.close()
        return None

    slot_id, service_date, service_time = slot

    # Create booking
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

    # Mark slot unavailable
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