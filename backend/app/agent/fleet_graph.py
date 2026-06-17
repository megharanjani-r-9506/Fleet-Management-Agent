from langgraph.graph import StateGraph, END

from app.database.db import get_connection
from app.services.booking_service import create_booking
from app.services.smart_scheduler import select_best_slot

from app.services.decision_service import (
    log_decision,
    create_notification
)

from app.services.fleet_service import find_replacement_vehicle
from app.services.delivery_service import (
    has_upcoming_delivery,
    reassign_delivery
)

from app.services.conflict_engine import check_universal_conflict


# -----------------------------
# STATE STRUCTURE
# -----------------------------
def init_state():
    return {
        "pending": [],
        "allocations": [],
        "decisions": []
    }


# -----------------------------
# NODE 1: FETCH PENDING
# -----------------------------
def fetch_pending(state):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, vehicle_id, risk_level
        FROM maintenance_schedule
        WHERE status = 'Pending'
        ORDER BY id ASC
    """)

    state["pending"] = cursor.fetchall()
    conn.close()

    print(f"[GRAPH] Pending: {len(state['pending'])}")

    return state


# -----------------------------
# NODE 2: RANK VEHICLES
# -----------------------------
def rank_vehicles(state):

    priority_map = {
        "Critical": 1,
        "Maintenance Required": 2,
        "Monitor": 3,
        "Healthy": 4
    }

    state["pending"].sort(
        key=lambda x: priority_map.get(x[2], 99)
    )

    print("\n[GRAPH] Ranked Order:")
    for _, vehicle_id, risk_level in state["pending"]:
        print(f"{vehicle_id} -> {risk_level}")

    return state


# -----------------------------
# NODE 3: DECISION BRAIN (UNIFIED ENGINE)
# -----------------------------
def decision_brain(state):

    print("\n[GRAPH] Running Decision Brain...")

    decisions = []

    for maintenance_id, vehicle_id, risk_level in state["pending"]:

        priority_map = {
            "Critical": 1,
            "Maintenance Required": 2,
            "Monitor": 3,
            "Healthy": 4
        }

        priority_score = priority_map.get(risk_level, 99)

        conflict = check_universal_conflict(vehicle_id, risk_level)
        delivery = has_upcoming_delivery(vehicle_id)

        decision = None
        reason = None

        # --------------------------------
        # CRITICAL CASE WITH CONFLICT
        # --------------------------------
        if risk_level == "Critical" and (conflict["has_conflict"] or delivery):

            if delivery:

                delivery_id, delivery_date, route = delivery

                replacement = find_replacement_vehicle(vehicle_id, delivery_date)

                if replacement:

                    reassign_delivery(vehicle_id, replacement)

                    decision = "Delivery Reassigned"
                    reason = f"Moved to {replacement} due to conflict"

                    create_notification(
                        "Delivery Reassigned",
                        f"{vehicle_id} reassigned to {replacement}"
                    )

                else:

                    decision = "Hold Delivery"
                    reason = "No replacement vehicle available"

                    create_notification(
                        "Delivery Held",
                        f"{vehicle_id} has no replacement available"
                    )

            else:

                decision = "Maintenance Delayed"
                reason = "Conflict detected but no delivery impact"

        # --------------------------------
        # MAINTENANCE REQUIRED CASE
        # --------------------------------
        elif risk_level == "Maintenance Required":

            if delivery:

                decision = "Schedule After Delivery"
                reason = "Maintenance deferred due to delivery"

            else:

                decision = "Schedule Maintenance"
                reason = "Safe to proceed"

        # --------------------------------
        # DEFAULT CASE
        # --------------------------------
        else:

            decision = "No Action Required"
            reason = "Vehicle is stable or low priority"

        # --------------------------------
        # LOG DECISION
        # --------------------------------
        log_decision(vehicle_id, risk_level, decision, reason)

        print(f"[GRAPH] Decision -> {vehicle_id} | {decision}")

        decisions.append({
            "vehicle_id": vehicle_id,
            "risk_level": risk_level,
            "priority_score": priority_score,
            "decision": decision,
            "reason": reason
        })

    state["decisions"] = decisions
    return state


# -----------------------------
# NODE 4: SLOT ALLOCATION
# -----------------------------
def allocate_slots(state):

    allocations = []

    print("\n[GRAPH] Allocating Slots...")

    for maintenance_id, vehicle_id, risk_level in state["pending"]:

        conflict = check_universal_conflict(vehicle_id, risk_level)

        if conflict["has_conflict"]:

            print(
                f"[GRAPH] Conflict -> "
                f"{vehicle_id} | {conflict['type']} | {conflict['details']}"
            )
            continue

        slot = select_best_slot(vehicle_id)

        if not slot:
            print(f"[GRAPH] No slot available for {vehicle_id}")
            continue

        slot_id, service_date, service_time = slot

        allocations.append({
            "maintenance_id": maintenance_id,
            "vehicle_id": vehicle_id,
            "risk_level": risk_level,
            "slot": slot
        })

        print(
            f"[GRAPH] Slot Selected -> "
            f"{vehicle_id}: {service_date} {service_time}"
        )

    state["allocations"] = allocations
    return state


# -----------------------------
# NODE 5: PROCESS BOOKINGS
# -----------------------------
def process_vehicle(state):

    conn = get_connection()
    cursor = conn.cursor()

    for item in state["allocations"]:

        maintenance_id = item["maintenance_id"]
        vehicle_id = item["vehicle_id"]
        slot_id, service_date, service_time = item["slot"]

        print(f"\n[GRAPH] Processing {vehicle_id}")

        booking = create_booking(vehicle_id, slot_id, service_date, service_time)

        if booking:

            cursor.execute("""
                UPDATE maintenance_schedule
                SET status = 'Booked'
                WHERE id = ?
            """, (maintenance_id,))

            conn.commit()

            print(
                f"[GRAPH] Booked {vehicle_id} -> "
                f"{service_date} {service_time}"
            )

    conn.close()
    return state


# -----------------------------
# BUILD GRAPH
# -----------------------------
graph = StateGraph(dict)

graph.add_node("fetch_pending", fetch_pending)
graph.add_node("rank_vehicles", rank_vehicles)
graph.add_node("decision_brain", decision_brain)
graph.add_node("allocate_slots", allocate_slots)
graph.add_node("process_vehicle", process_vehicle)

graph.set_entry_point("fetch_pending")

graph.add_edge("fetch_pending", "rank_vehicles")
graph.add_edge("rank_vehicles", "decision_brain")
graph.add_edge("decision_brain", "allocate_slots")
graph.add_edge("allocate_slots", "process_vehicle")
graph.add_edge("process_vehicle", END)

app = graph.compile()


# -----------------------------
# RUNNER
# -----------------------------
def run_fleet_graph():

    print("[GRAPH] Starting fleet orchestration...")

    state = init_state()

    app.invoke(state)

    print("\n[GRAPH] Completed cycle")


if __name__ == "__main__":
    run_fleet_graph()