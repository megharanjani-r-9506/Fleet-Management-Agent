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
        "current_vehicle": None,
        "selected_slot": None
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
# NODE 2: PROCESS ONE VEHICLE
# -----------------------------
def process_vehicle(state):

    conn = get_connection()
    cursor = conn.cursor()

    for maintenance_id, vehicle_id, risk_level in state["pending"]:

        print(f"[GRAPH] Processing {vehicle_id}")

        # -------------------------
        # CHECK SLOT
        # -------------------------
        slot = select_best_slot(vehicle_id)

        if not slot:
            print(f"[GRAPH] No slot for {vehicle_id}")
            continue

        slot_id, service_date, service_time = slot

        # -------------------------
        # CREATE BOOKING
        # -------------------------
        booking = create_booking(vehicle_id)

        if booking:

            cursor.execute("""
                UPDATE maintenance_schedule
                SET status = 'Booked'
                WHERE id = ?
            """, (maintenance_id,))

            conn.commit()

            print(f"[GRAPH] Booked {vehicle_id} -> {service_date} {service_time}")

    conn.close()
    return state

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
# BUILD GRAPH
# -----------------------------
graph = StateGraph(dict)

graph.add_node("fetch_pending", fetch_pending)
graph.add_node("rank_vehicles", rank_vehicles)
graph.add_node("process_vehicle", process_vehicle)

graph.set_entry_point("fetch_pending")

graph.add_edge("fetch_pending", "rank_vehicles")
graph.add_edge("rank_vehicles", "process_vehicle")
graph.add_edge("process_vehicle", END)

app = graph.compile()


# -----------------------------
# RUNNER
# -----------------------------
def run_fleet_graph():

    print("[GRAPH] Starting fleet orchestration...")

    state = init_state()
    app.invoke(state)

    print("[GRAPH] Completed cycle")


if __name__ == "__main__":
    run_fleet_graph()