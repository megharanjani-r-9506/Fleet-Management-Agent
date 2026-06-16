from app.database.db import get_connection


def has_pending_maintenance(vehicle_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 FROM maintenance_schedule
        WHERE vehicle_id = ? AND status = 'Pending'
    """, (vehicle_id,))

    result = cursor.fetchone()
    conn.close()

    return result is not None


def schedule_maintenance(vehicle_id, risk_level):

    if risk_level in ["Healthy", "Monitor"]:
        return None

    if has_pending_maintenance(vehicle_id):
        return {"message": "Already scheduled"}

    if risk_level == "Critical":
        recommendation = "Schedule maintenance within 24 hours"
        priority = "High"
    else:
        recommendation = "Schedule maintenance within 3 days"
        priority = "Medium"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO maintenance_schedule (
            vehicle_id,
            risk_level,
            recommendation,
            priority,
            status
        )
        VALUES (?, ?, ?, ?, 'Pending')
    """, (
        vehicle_id,
        risk_level,
        recommendation,
        priority
    ))

    conn.commit()
    conn.close()

    return {
        "vehicle_id": vehicle_id,
        "status": "Pending"
    }