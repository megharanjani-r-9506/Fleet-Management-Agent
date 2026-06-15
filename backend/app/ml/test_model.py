import joblib
import pandas as pd

model = joblib.load(
    "app/models/failure_model.pkl"
)

sample = pd.DataFrame([
    {
        "Air temperature [K]": 310,
        "Process temperature [K]": 320,
        "Rotational speed [rpm]": 3000,
        "Torque [Nm]": 80,
        "Tool wear [min]": 250
    }
])

probability = model.predict_proba(sample)

failure_probability = probability[0][1] * 100
health_score = 100 - failure_probability

if health_score > 80:
    risk_level = "Healthy"

elif health_score > 50:
    risk_level = "Monitor"

elif health_score > 20:
    risk_level = "Maintenance Required"

else:
    risk_level = "Critical"
print("Failure Probability:", round(failure_probability, 2), "%")
print("Health Score:", round(health_score, 2))
print("Risk Level:", risk_level)