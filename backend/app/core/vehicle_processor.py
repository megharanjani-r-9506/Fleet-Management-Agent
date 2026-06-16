from app.ml.predictor import predict_vehicle_health
from app.services.maintenance_scheduler import schedule_maintenance
from app.database.db import get_connection


def save_prediction(vehicle_id, result):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            vehicle_id,
            health_score,
            failure_probability,
            risk_level
        )
        VALUES (?, ?, ?, ?)
    """, (
        vehicle_id,
        result["health_score"],
        result["failure_probability"],
        result["risk_level"]
    ))

    conn.commit()
    conn.close()


def process_vehicle_event(telemetry):

    # Step 1: ML Prediction
    result = predict_vehicle_health(
        ambient_temp=telemetry["ambient_temp"],
        engine_temp=telemetry["engine_temp"],
        engine_rpm=telemetry["engine_rpm"],
        engine_load=telemetry["engine_load"],
        operating_hours=telemetry["operating_hours"],
        mileage=telemetry["mileage"]
    )

    # Step 2: Maintenance logic
    maintenance = schedule_maintenance(
        vehicle_id=telemetry["vehicle_id"],
        risk_level=result["risk_level"]
    )

    # Step 3: SAVE prediction (FIXED)
    save_prediction(
        telemetry["vehicle_id"],
        result
    )

    return {
        "telemetry": telemetry,
        "prediction": result,
        "maintenance": maintenance
    }