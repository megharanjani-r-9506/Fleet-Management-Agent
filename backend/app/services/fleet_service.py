from datetime import datetime, timedelta

from app.database.db import get_connection

from app.services.ai_replacement_agent import (
    choose_replacement_vehicle
)


def find_replacement_vehicle(
    excluded_vehicle,
    delivery_date
):

    conn = get_connection()
    cursor = conn.cursor()

    target_date = datetime.strptime(
        delivery_date,
        "%Y-%m-%d"
    )

    # --------------------------------
    # Vehicles already delivering
    # on the same date
    # --------------------------------
    cursor.execute("""
        SELECT vehicle_id
        FROM delivery_schedule
        WHERE delivery_date = ?
        AND status = 'Scheduled'
    """, (delivery_date,))

    assigned_today = {
        row[0]
        for row in cursor.fetchall()
    }

    # --------------------------------
    # Candidate vehicles
    # --------------------------------
    cursor.execute("""
        SELECT vehicle_id
        FROM vehicles
        WHERE vehicle_id != ?
    """, (excluded_vehicle,))

    candidates = cursor.fetchall()

    candidate_vehicles = []

    for (vehicle_id,) in candidates:

        # -----------------------------
        # Skip vehicles already
        # assigned on same day
        # -----------------------------
        if vehicle_id in assigned_today:
            continue

        # -----------------------------
        # Check maintenance bookings
        # within ±1 day window
        # -----------------------------
        start_window = (
            target_date - timedelta(days=1)
        ).strftime("%Y-%m-%d")

        end_window = (
            target_date + timedelta(days=1)
        ).strftime("%Y-%m-%d")

        cursor.execute("""
            SELECT COUNT(*)
            FROM service_bookings
            WHERE vehicle_id = ?
            AND service_date BETWEEN ? AND ?
        """, (
            vehicle_id,
            start_window,
            end_window
        ))

        maintenance_count = cursor.fetchone()[0]

        # Reject maintenance-conflicted vehicles
        if maintenance_count > 0:

            print(
                f"[GRAPH] Rejecting "
                f"{vehicle_id} "
                f"(maintenance scheduled)"
            )

            continue

        # -----------------------------
        # Future delivery workload
        # -----------------------------
        cursor.execute("""
            SELECT delivery_date
            FROM delivery_schedule
            WHERE vehicle_id = ?
            AND status = 'Scheduled'
            ORDER BY delivery_date ASC
        """, (vehicle_id,))

        future_deliveries = cursor.fetchall()

        cursor.execute("""
            SELECT risk_level
            FROM predictions
            WHERE vehicle_id = ?
            ORDER BY id DESC
            LIMIT 1
        """, (vehicle_id,))

        prediction = cursor.fetchone()

        risk_level = (
            prediction[0]
            if prediction
            else "Unknown"
        )

        candidate_vehicles.append({
            "vehicle_id": vehicle_id,
            "future_deliveries": len(future_deliveries),
            "maintenance_booked": False,
            "risk_level": risk_level
        })
    conn.close()

    # --------------------------------
    # No candidates available
    # --------------------------------
    if not candidate_vehicles:

        print(
            "[GRAPH] No suitable replacement found"
        )

        return None

    # --------------------------------
    # Gemini chooses best vehicle
    # --------------------------------
    result = choose_replacement_vehicle(
        excluded_vehicle,
        "Critical",
        delivery_date,
        candidate_vehicles
    )

    recommended_vehicle = result["vehicle_id"]

    print(
        f"[AI] Gemini Selected -> "
        f"{recommended_vehicle}"
    )

    print(
        f"[AI] Reason -> "
        f"{result['reason']}"
    )

    return recommended_vehicle