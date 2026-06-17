from app.database.db import get_connection

def log_decision(
    vehicle_id,
    risk_level,
    decision,
    reason
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO agent_decisions (
            vehicle_id,
            risk_level,
            decision,
            reason
        )
        VALUES (?, ?, ?, ?)
    """, (
        vehicle_id,
        risk_level,
        decision,
        reason
    ))

    conn.commit()
    conn.close()


def create_notification(
    title,
    message
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO notifications (
            title,
            message
        )
        VALUES (?, ?)
    """, (
        title,
        message
    ))

    conn.commit()
    conn.close()