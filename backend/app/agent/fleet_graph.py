from langgraph.graph import StateGraph, END

from app.database.db import get_connection
from app.services.booking_service import create_booking
from app.services.smart_scheduler import get_available_slots

from app.services.ai_scheduler_agent import (
    choose_maintenance_slot
)
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
from app.services.notification_service import send_email

from app.services.ai_decision_agent import (
    make_maintenance_decision
)

from app.services.notification_service import (
    send_email,
    build_delivery_reassigned_email,
    build_maintenance_email,
    build_delivery_hold_email,
    build_maintenance_deferred_email,
    build_maintenance_delayed_email
)
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

def get_failure_probability(vehicle_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT failure_probability
        FROM predictions
        WHERE vehicle_id = ?
        ORDER BY id DESC
        LIMIT 1
    """,
        (vehicle_id,),
    )

    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0]

    return 0


def get_upcoming_delivery_count(vehicle_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM delivery_schedule
        WHERE vehicle_id = ?
        AND status = 'Scheduled'
    """,
        (vehicle_id,),
    )

    count = cursor.fetchone()[0]
    conn.close()

    return count
# -----------------------------
# NODE 3: DECISION BRAIN
# -----------------------------
def decision_brain(state):

    print("\n[GRAPH] Running Decision Brain...")

    decisions = []

    for maintenance_id, vehicle_id, risk_level in state["pending"]:

        delivery = has_upcoming_delivery(vehicle_id)

        replacement = None
        replacement_available = False

        if delivery:

            delivery_id, delivery_date, route = delivery

            replacement = find_replacement_vehicle(
                vehicle_id,
                delivery_date
            )

            replacement_available = (
                replacement is not None
            )

        # --------------------------------
        # AI Decision Agent
        # --------------------------------
        failure_probability = get_failure_probability(
            vehicle_id
        )

        upcoming_delivery_count = (
            get_upcoming_delivery_count(
                vehicle_id
            )
        )

        replacement_vehicle_count = 1 if replacement_available else 0
        
        ai_result = make_maintenance_decision(
            vehicle_id=vehicle_id,
            risk_level=risk_level,
            has_delivery=bool(delivery),
            replacement_available=replacement_available,
            failure_probability=failure_probability,
            upcoming_delivery_count=upcoming_delivery_count,
            replacement_vehicle_count=replacement_vehicle_count
        )

        decision = ai_result["decision"]
        reason = ai_result["reason"]
        confidence = ai_result.get(
            "confidence",
            0
        )

        print(
            f"[AI] {vehicle_id} -> "
            f"{decision} "
            f"(Confidence={confidence}%)"
        )

        # --------------------------------
        # Execute Decision
        # --------------------------------

        if decision == "Delivery Reassigned":

            delivery_id, delivery_date, route = delivery

            reassign_delivery(
                vehicle_id,
                replacement
            )

            create_notification(
                "Delivery Reassigned",
                f"{vehicle_id} reassigned to {replacement}"
            )

            send_email(
                "🚚 Delivery Reassigned",
                build_delivery_reassigned_email(
                    vehicle_id,
                    replacement,
                    route,
                    delivery_date
                )
            )

        elif decision == "Hold Delivery":

            create_notification(
                "Delivery Held",
                f"{vehicle_id} has no replacement available"
            )

            send_email(
                "⛔ Delivery Held",
                build_delivery_hold_email(
                    vehicle_id
                )
            )

        elif decision == "Schedule Maintenance":

            send_email(
                "🛠️ Maintenance Approved",
                build_maintenance_email(
                    vehicle_id
                )
            )

        elif decision == "Schedule After Delivery":

            send_email(
                "📅 Maintenance Deferred",
                build_maintenance_deferred_email(
                    vehicle_id
                )
            )

        elif decision == "Maintenance Delayed":

            send_email(
                "⚠️ Maintenance Delayed",
                build_maintenance_delayed_email(
                    vehicle_id
                )
            )

        # --------------------------------
        # LOG DECISION
        # --------------------------------

        log_decision(
            vehicle_id,
            risk_level,
            decision,
            reason
        )

        print(
            f"[GRAPH] Decision -> "
            f"{vehicle_id} | {decision}"
        )

        decisions.append({
            "vehicle_id": vehicle_id,
            "risk_level": risk_level,
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
                f"{vehicle_id} | "
                f"{conflict['type']} | "
                f"{conflict['details']}"
            )
            continue

        # --------------------------------
        # Get ALL available slots
        # --------------------------------
        available_slots = get_available_slots(vehicle_id)

        if not available_slots:
            print(f"[GRAPH] No slot available for {vehicle_id}")
            continue

        # --------------------------------
        # AI Scheduler Agent
        # --------------------------------
        ai_choice = choose_maintenance_slot(
            vehicle_id, risk_level, available_slots
        )

        chosen_slot_id = ai_choice["slot_id"]

        print(f"[AI Scheduler] {vehicle_id} -> Slot {chosen_slot_id}")

        # --------------------------------
        # Find chosen slot
        # --------------------------------
        selected_slot = None

        for slot in available_slots:
            if slot["slot_id"] == chosen_slot_id:
                selected_slot = slot
                break

        # Fallback
        if not selected_slot:
            selected_slot = available_slots[0]
            print("[GRAPH] AI selected invalid slot. Using fallback.")

        slot_id = selected_slot["slot_id"]
        service_date = selected_slot["date"]
        service_time = selected_slot["time"]

        allocations.append(
            {
                "maintenance_id": maintenance_id,
                "vehicle_id": vehicle_id,
                "risk_level": risk_level,
                "slot": (slot_id, service_date, service_time),
            }
        )

        print(
            f"[GRAPH] Slot Selected -> "
            f"{vehicle_id}: "
            f"{service_date} "
            f"{service_time}"
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

            # 📧 EMAIL TRIGGER (MAINTENANCE BOOKED)
            send_email(
                "🛠️ Maintenance Booked",
                f"Vehicle {vehicle_id} scheduled for maintenance on "
                f"{service_date} at {service_time}"
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