from app.database.db import get_connection
from app.services.booking_service import create_booking
from app.services.delivery_service import has_scheduled_delivery
from app.services.fleet_service import find_replacement_vehicle
from app.services.reassignment_service import reassign_delivery
def schedule_maintenance(vehicle_id, risk_level):

    if risk_level == "Healthy":
        return None

    if risk_level == "Monitor":
        return None

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
    VALUES (?, ?, ?, ?, ?)
    """, (
        vehicle_id,
        risk_level,
        recommendation,
        priority,
        "Pending"
    ))

    conn.commit()
    conn.close()

    if has_scheduled_delivery(vehicle_id):

        print(
            f"WARNING: {vehicle_id} has a scheduled delivery."
        )

        replacement = find_replacement_vehicle(vehicle_id)

        if replacement:

                print(
                    f"Replacement Vehicle Found: {replacement}"
                )

                moved = reassign_delivery(
                    vehicle_id,
                    replacement
                )

                print(
                    f"Deliveries Reassigned: {moved}"
                )

                booking = create_booking(vehicle_id)

        else:

            print(
                    "No replacement vehicle available."
            )

            booking = None

    else:

        booking = create_booking(vehicle_id)

    return {
        "recommendation": recommendation,
        "priority": priority,
        "booking": booking
    }