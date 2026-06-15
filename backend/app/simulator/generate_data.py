import random
import time

from app.simulator.save_telemetry import save_telemetry
from app.core.vehicle_processor import process_vehicle_event


vehicle = {
    "vehicle_id": "TRK001",
    "ambient_temp": 30,
    "engine_temp": 90,
    "engine_rpm": 2000,
    "engine_load": 50,
    "operating_hours": 2000,
    "mileage": 42000
}


def generate_vehicle_data():

    vehicle["ambient_temp"] += random.uniform(-0.2, 0.2)
    vehicle["engine_temp"] += random.uniform(-2, 2)
    vehicle["engine_rpm"] += random.randint(-100, 100)
    vehicle["engine_load"] += random.uniform(-5, 5)
    vehicle["operating_hours"] += 1
    vehicle["mileage"] += random.randint(5, 20)

    return {
        "vehicle_id": vehicle["vehicle_id"],
        "ambient_temp": round(vehicle["ambient_temp"], 2),
        "engine_temp": round(vehicle["engine_temp"], 2),
        "engine_rpm": int(vehicle["engine_rpm"]),
        "engine_load": round(vehicle["engine_load"], 2),
        "operating_hours": vehicle["operating_hours"],
        "mileage": vehicle["mileage"]
    }


if __name__ == "__main__":

    while True:

        # 1. Generate telemetry
        data = generate_vehicle_data()

        # 2. Save telemetry to DB
        save_telemetry(data)

        # 3. Run FULL agent pipeline (ONLY ONE ENTRY POINT)
        result = process_vehicle_event(data)

        # 4. Print clean structured output
        print("Telemetry:", result["telemetry"])
        print("Prediction:", result["prediction"])
        print("Maintenance:", result["maintenance"])
        print("-" * 50)

        time.sleep(5)