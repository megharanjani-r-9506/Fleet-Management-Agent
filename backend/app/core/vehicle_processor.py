from app.ml.predictor import predict_vehicle_health
from app.services.maintenance_scheduler import schedule_maintenance


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

    # Step 2: Maintenance + Fleet Logic (already inside scheduler)
    maintenance = schedule_maintenance(
        vehicle_id=telemetry["vehicle_id"],
        risk_level=result["risk_level"]
    )

    return {
        "telemetry": telemetry,
        "prediction": result,
        "maintenance": maintenance
    }