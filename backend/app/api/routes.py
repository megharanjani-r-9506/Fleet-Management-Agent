from fastapi import APIRouter
from app.database.db import get_connection
from app.simulator.generate_data import (
    vehicles,
    generate_telemetry
)
from app.reset import reset_demo
from app.agent.fleet_graph import run_fleet_graph
from app.simulator.save_telemetry import save_telemetry
from app.core.vehicle_processor import process_vehicle_event

router = APIRouter()


# -----------------------------
# VEHICLES
# -----------------------------
@router.get("/vehicles")
def get_vehicles():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles")

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        return [dict(zip(columns, row)) for row in rows]

    finally:
        conn.close()


# -----------------------------
# PREDICTIONS
# -----------------------------
@router.get("/predictions")
def get_predictions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM predictions
        ORDER BY id DESC
    """)

    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    conn.close()

    return [dict(zip(columns, row)) for row in rows]


# -----------------------------
# MAINTENANCE
# -----------------------------
@router.get("/maintenance")
def get_maintenance():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM maintenance_schedule
        ORDER BY id DESC
    """)

    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    conn.close()

    return [dict(zip(columns, row)) for row in rows]


# -----------------------------
# BOOKINGS
# -----------------------------
@router.get("/bookings")
def get_bookings():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT *
            FROM service_bookings
            ORDER BY id DESC
        """)

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        return [dict(zip(columns, row)) for row in rows]

    finally:
        conn.close()


# -----------------------------
# DELIVERIES
# -----------------------------
@router.get("/deliveries")
def get_deliveries():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM delivery_schedule
        ORDER BY id DESC
    """)

    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    conn.close()

    return [dict(zip(columns, row)) for row in rows]


# -----------------------------
# SERVICE SLOTS
# -----------------------------
@router.get("/service-slots")
def get_service_slots():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM service_slots
        ORDER BY id DESC
    """)

    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    conn.close()

    return [dict(zip(columns, row)) for row in rows]

@router.get("/decisions")
def get_decisions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            vehicle_id,
            risk_level,
            decision,
            reason,
            created_at
        FROM agent_decisions
        ORDER BY id DESC
        LIMIT 20
    """)

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "vehicle_id": row[0],
            "risk_level": row[1],
            "decision": row[2],
            "reason": row[3],
            "created_at": row[4]
        }
        for row in rows
    ]

@router.get("/notifications")
def get_notifications():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, message, status, created_at
        FROM notifications
        ORDER BY id DESC
        LIMIT 20
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "title": r[1],
            "message": r[2],
            "status": r[3],
            "created_at": r[4]
        }
        for r in rows
    ]

@router.post("/generate-telemetry")
def generate_telemetry_now():

    results = []

    for vehicle in vehicles:

        data = generate_telemetry(
            vehicle["vehicle_id"]
        )

        save_telemetry(data)

        prediction = process_vehicle_event(data)

        results.append({
            "vehicle_id": data["vehicle_id"],
            "prediction": prediction["prediction"]
        })
        # Run the complete AI workflow

    return {
        "message": "Telemetry generated successfully",
        "vehicles_processed": len(results),
        "results": results
    }

@router.post("/reset-demo")
def reset_demo_endpoint():

    reset_demo()

    return {
        "message": "Demo environment reset successfully."
    }

@router.post("/run-ai-agents")
def run_ai_agents():

    run_fleet_graph()

    return {
        "message": "AI agents executed successfully."
    }