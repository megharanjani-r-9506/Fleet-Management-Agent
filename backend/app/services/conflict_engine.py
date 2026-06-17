from app.services.delivery_service import has_upcoming_delivery
from app.database.db import get_connection


# -----------------------------
# UNIVERSAL CONFLICT ENGINE
# -----------------------------
def check_universal_conflict(vehicle_id, risk_level):
    """
    Returns:
        dict {
            "has_conflict": bool,
            "type": str,
            "details": str
        }
    """

    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------------
    # 1. CHECK EXISTING BOOKING
    # -----------------------------------
    cursor.execute("""
        SELECT 1 FROM service_bookings
        WHERE vehicle_id = ?
        LIMIT 1
    """, (vehicle_id,))

    if cursor.fetchone():
        conn.close()
        return {
            "has_conflict": True,
            "type": "Already Booked",
            "details": "Vehicle already has a maintenance booking"
        }

    # -----------------------------------
    # 2. CHECK DELIVERY CONFLICT
    # -----------------------------------
    delivery = has_upcoming_delivery(vehicle_id)

    if delivery:
        delivery_id, delivery_date, route = delivery

        conn.close()
        return {
            "has_conflict": True,
            "type": "Delivery Conflict",
            "details": f"Delivery scheduled on {delivery_date} ({route})"
        }

    # -----------------------------------
    # 3. NO CONFLICT
    # -----------------------------------
    conn.close()

    return {
        "has_conflict": False,
        "type": "None",
        "details": "No conflicts found"
    }