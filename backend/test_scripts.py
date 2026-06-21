from app.database.db import get_connection

conn = get_connection()
cursor = conn.cursor()

# -----------------------------------------------------------------------------
# CLEAN TEST DATA
# -----------------------------------------------------------------------------
cursor.execute("DELETE FROM maintenance_schedule")
cursor.execute("DELETE FROM delivery_schedule")
cursor.execute("DELETE FROM service_bookings")

# -----------------------------------------------------------------------------
# PREDICTIONS
# -----------------------------------------------------------------------------
cursor.execute(
    """
    INSERT INTO predictions (
        vehicle_id,
        health_score,
        failure_probability,
        risk_level
    )
    VALUES (?, ?, ?, ?)
    """,
    ("TRK003", 5, 95, "Critical"),
)

cursor.execute(
    """
    INSERT INTO predictions (
        vehicle_id,
        health_score,
        failure_probability,
        risk_level
    )
    VALUES (?, ?, ?, ?)
    """,
    ("TRK001", 65, 35, "Monitor"),
)

cursor.execute(
    """
    INSERT INTO predictions (
        vehicle_id,
        health_score,
        failure_probability,
        risk_level
    )
    VALUES (?, ?, ?, ?)
    """,
    ("TRK004", 90, 10, "Healthy"),
)

cursor.execute(
    """
    INSERT INTO predictions (
        vehicle_id,
        health_score,
        failure_probability,
        risk_level
    )
    VALUES (?, ?, ?, ?)
    """,
    ("TRK005", 20, 80, "Maintenance Required"),
)

# -----------------------------------------------------------------------------
# MAINTENANCE SCHEDULE
# -----------------------------------------------------------------------------
cursor.execute(
    """
    INSERT INTO maintenance_schedule (
        vehicle_id,
        risk_level,
        status
    )
    VALUES (?, ?, ?)
    """,
    ("TRK003", "Critical", "Pending"),
)

# -----------------------------------------------------------------------------
# DELIVERIES
# -----------------------------------------------------------------------------

# Critical vehicle has delivery
cursor.execute(
    """
    INSERT INTO delivery_schedule (
        vehicle_id,
        route,
        delivery_date,
        status
    )
    VALUES (?, ?, ?, ?)
    """,
    ("TRK003", "Chennai Route", "2026-06-22", "Scheduled"),
)

# Busy vehicle
cursor.execute(
    """
    INSERT INTO delivery_schedule (
        vehicle_id,
        route,
        delivery_date,
        status
    )
    VALUES (?, ?, ?, ?)
    """,
    ("TRK001", "Madurai Route", "2026-06-23", "Scheduled"),
)

cursor.execute(
    """
    INSERT INTO delivery_schedule (
        vehicle_id,
        route,
        delivery_date,
        status
    )
    VALUES (?, ?, ?, ?)
    """,
    ("TRK001", "Salem Route", "2026-06-24", "Scheduled"),
)

cursor.execute(
    """
    INSERT INTO delivery_schedule (
        vehicle_id,
        route,
        delivery_date,
        status
    )
    VALUES (?, ?, ?, ?)
    """,
    ("TRK001", "Coimbatore Route", "2026-06-25", "Scheduled"),
)

# -----------------------------------------------------------------------------
# MAINTENANCE BOOKING (makes TRK005 unattractive)
# -----------------------------------------------------------------------------
cursor.execute(
    """
    INSERT INTO service_bookings (
        vehicle_id,
        service_date,
        service_time,
        status
    )
    VALUES (?, ?, ?, ?)
    """,
    ("TRK005", "2026-06-22", "09:00", "Booked"),
)

conn.commit()
conn.close()

print("================================")
print("TEST DATA CREATED")
print("================================")
print("TRK003 -> Critical")
print("TRK003 -> Upcoming Delivery")
print("TRK004 -> Healthy Replacement")
print("TRK001 -> Busy Vehicle")
print("TRK005 -> Maintenance Booked")
print("================================")