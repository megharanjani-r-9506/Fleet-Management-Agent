from app.ml.predictor import predict_vehicle_health
from app.database.db import get_connection


def save_prediction(telemetry):

    result = predict_vehicle_health(
    ambient_temp=telemetry["ambient_temp"],
    engine_temp=telemetry["engine_temp"],
    engine_rpm=telemetry["engine_rpm"],
    engine_load=telemetry["engine_load"],
    operating_hours=telemetry["operating_hours"],
    mileage=telemetry["mileage"]
)

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
        telemetry["vehicle_id"],
        result["health_score"],
        result["failure_probability"],
        result["risk_level"]
    ))

    conn.commit()
    conn.close()

    return result