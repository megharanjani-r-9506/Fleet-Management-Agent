import joblib
import pandas as pd


model = joblib.load("app/models/failure_model.pkl")


def predict_vehicle_health(
    ambient_temp,
    engine_temp,
    engine_rpm,
    engine_load,
    operating_hours,
    mileage
):

    sample = pd.DataFrame([
        {
            "ambient_temp": ambient_temp,
            "engine_temp": engine_temp,
            "engine_rpm": engine_rpm,
            "engine_load": engine_load,
            "operating_hours": operating_hours,
            "mileage": mileage
        }
    ])

    probability = model.predict_proba(sample)

    failure_probability = probability[0][1] * 100

    health_score = 100 - failure_probability

    if health_score > 40:
        risk_level = "Healthy"

    elif health_score > 25:
        risk_level = "Monitor"

    elif health_score > 10:
        risk_level = "Maintenance Required"

    else:
        risk_level = "Critical"

    return {
        "health_score": float(round(health_score, 2)),
        "failure_probability": float(round(failure_probability, 2)),
        "risk_level": risk_level
    }