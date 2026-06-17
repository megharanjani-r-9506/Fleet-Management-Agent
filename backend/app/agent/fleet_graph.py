from langgraph.graph import StateGraph, END

from app.database.db import get_connection
from app.services.booking_service import create_booking
from app.services.smart_scheduler import select_best_slot


# -----------------------------
# STATE STRUCTURE
# -----------------------------
def init_state():
    return {
        "pending": [],
        "allocations": []
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
# NODE 3: ALLOCATE SLOTS
# -----------------------------
def allocate_slots(state):

    conn = get_connection()
    cursor = conn.cursor()

    allocations = []

    print("\n[GRAPH] Allocating Slots...")

    # Get all available slots once
    cursor.execute("""
        SELECT id, service_date, service_time
        FROM service_slots
        WHERE available = 1
        ORDER BY service_date ASC, id ASC
    """)

    available_slots = cursor.fetchall()

    slot_index = 0

    for maintenance_id, vehicle_id, risk_level in state["pending"]:

        # No more slots
        if slot_index >= len(available_slots):

            print(
                f"[GRAPH] No slot available for {vehicle_id}"
            )

            continue

        slot = available_slots[slot_index]
        slot_index += 1

        slot_id, service_date, service_time = slot

        allocations.append({
            "maintenance_id": maintenance_id,
            "vehicle_id": vehicle_id,
            "risk_level": risk_level,
            "slot": slot
        })

        print(
            f"[GRAPH] Slot Selected -> "
            f"{vehicle_id}: "
            f"{service_date} {service_time}"
        )

    conn.close()

    state["allocations"] = allocations

    return state

# -----------------------------
# NODE 4: PROCESS BOOKINGS
# -----------------------------
def process_vehicle(state):

    conn = get_connection()
    cursor = conn.cursor()

    for item in state["allocations"]:

        maintenance_id = item["maintenance_id"]
        vehicle_id = item["vehicle_id"]

        slot_id, service_date, service_time = item["slot"]

        print(f"\n[GRAPH] Processing {vehicle_id}")

        slot_id, service_date, service_time = item["slot"]

        booking = create_booking(vehicle_id,slot_id,service_date,service_time)

        if booking:

            cursor.execute("""
                UPDATE maintenance_schedule
                SET status = 'Booked'
                WHERE id = ?
            """, (maintenance_id,))

            conn.commit()

            print(
                f"[GRAPH] Booked "
                f"{vehicle_id} -> "
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
graph.add_node("allocate_slots", allocate_slots)
graph.add_node("process_vehicle", process_vehicle)

graph.set_entry_point("fetch_pending")

graph.add_edge("fetch_pending", "rank_vehicles")
graph.add_edge("rank_vehicles", "allocate_slots")
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