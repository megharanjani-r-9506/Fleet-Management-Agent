from app.database.db import get_connection


def reset_demo():

    conn = get_connection()
    cur = conn.cursor()

    # Agent outputs
    cur.execute("DELETE FROM agent_decisions")
    cur.execute("DELETE FROM notifications")

    # Maintenance workflow
    cur.execute("DELETE FROM maintenance_schedule")
    cur.execute("DELETE FROM service_bookings")

    # Deliveries
    cur.execute("DELETE FROM delivery_schedule")

    # Restore demo deliveries
    deliveries = [
        ("TRK001", "2026-06-15", "Chennai-Coimbatore", "Scheduled"),
        ("TRK004", "2026-06-15", "Chennai-Madurai", "Scheduled")
    ]

    cur.executemany("""
    INSERT INTO delivery_schedule (
        vehicle_id,
        delivery_date,
        route,
        status
    )
    VALUES (?, ?, ?, ?)
    """, deliveries)

    # Predictions
    cur.execute("DELETE FROM predictions")

    # Make all service slots available again
    cur.execute("""
        UPDATE service_slots
        SET available = 1
    """)

    conn.commit()
    conn.close()

    print("TEST ENVIRONMENT RESET")


if __name__ == "__main__":
    reset_demo()