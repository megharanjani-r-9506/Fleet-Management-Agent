from datetime import datetime, timedelta

from app.database.db import get_connection


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

    scored_candidates = []

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

        # -----------------------------
        # Scoring Logic
        # -----------------------------
        if not future_deliveries:

            score = 100

        else:

            next_delivery = datetime.strptime(
                future_deliveries[0][0],
                "%Y-%m-%d"
            )

            days_gap = (
                next_delivery - target_date
            ).days

            if days_gap >= 7:
                score = 80

            elif days_gap >= 3:
                score = 50

            elif days_gap >= 1:
                score = 10

            else:
                score = 0

        scored_candidates.append({
            "vehicle_id": vehicle_id,
            "score": score
        })

    conn.close()

    # -----------------------------
    # No replacement available
    # -----------------------------
    if not scored_candidates:

        print(
            "[GRAPH] No suitable replacement found"
        )

        return None

    # -----------------------------
    # Highest score wins
    # -----------------------------
    scored_candidates.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    best_vehicle = scored_candidates[0]

    print(
        f"[GRAPH] Best Replacement -> "
        f"{best_vehicle['vehicle_id']} "
        f"(Score={best_vehicle['score']})"
    )

    return best_vehicle["vehicle_id"]