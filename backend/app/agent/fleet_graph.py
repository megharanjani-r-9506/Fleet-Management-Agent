from langgraph.graph import StateGraph, END
from app.database.db import get_connection
from app.services.booking_service import create_booking
from app.services.smart_scheduler import select_best_slot
# -----------------------------
# NODE 1: GET PENDING MAINTENANCE
# -----------------------------
def fetch_pending(state):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, vehicle_id
        FROM maintenance_schedule
        WHERE status = 'Pending'
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()

    print("[DEBUG] Pending rows:", rows)   # 🔥 ADD THIS

    state["pending"] = rows
    conn.close()

    return state
# -----------------------------
# NODE 2: PROCESS BOOKINGS
# -----------------------------
def process_bookings(state):

    conn = get_connection()
    cursor = conn.cursor()

    for maintenance_id, vehicle_id in state.get("pending", []):

        print(f"[GRAPH] Processing {vehicle_id}")

        # -----------------------------
        # USE SMART SCHEDULER (NEW)
        # -----------------------------
        slot = select_best_slot(vehicle_id)

        if not slot:
            print(f"[GRAPH] No slot available for {vehicle_id}")
            continue

        slot_id, service_date, service_time = slot

        # -----------------------------
        # CREATE BOOKING (MANUAL INSERT NOW)
        # -----------------------------
        cursor.execute("""
            INSERT INTO service_bookings (
                vehicle_id,
                service_date,
                service_time,
                status
            )
            VALUES (?, ?, ?, 'Booked')
        """, (
            vehicle_id,
            service_date,
            service_time
        ))

        # -----------------------------
        # MARK SLOT AS USED
        # -----------------------------
        cursor.execute("""
            UPDATE service_slots
            SET available = 0
            WHERE id = ?
        """, (slot_id,))

        # -----------------------------
        # UPDATE MAINTENANCE STATUS
        # -----------------------------
        cursor.execute("""
            UPDATE maintenance_schedule
            SET status = 'Booked'
            WHERE id = ?
        """, (maintenance_id,))

        conn.commit()

        print(f"[GRAPH] Booked {vehicle_id} -> {service_date} {service_time}")

    conn.close()
    return state
# -----------------------------
# BUILD GRAPH
# -----------------------------
graph = StateGraph(dict)

graph.add_node("fetch_pending", fetch_pending)
graph.add_node("process_bookings", process_bookings)

graph.set_entry_point("fetch_pending")
graph.add_edge("fetch_pending", "process_bookings")
graph.add_edge("process_bookings", END)

app = graph.compile()


# -----------------------------
# RUNNER
# -----------------------------
def run_fleet_graph():

    print("[GRAPH] Starting fleet orchestration...")

    result = app.invoke({})

    print("[GRAPH] Completed cycle")


if __name__ == "__main__":
    run_fleet_graph()