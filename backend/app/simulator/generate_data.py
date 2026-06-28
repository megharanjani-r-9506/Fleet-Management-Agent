import random
import time

from app.simulator.save_telemetry import save_telemetry
from app.core.vehicle_processor import process_vehicle_event
from app.simulator.vehicle_state import vehicle_state

vehicles = [

    # HEALTHY
    {
        "vehicle_id": "TRK001",
        "ambient_temp": 25,
        "engine_temp": 75,
        "engine_rpm": 1500,
        "engine_load": 30,
        "operating_hours": 500,
        "mileage": 10000
    },

    # MONITOR
    {
        "vehicle_id": "TRK002",
        "ambient_temp": 30,
        "engine_temp": 90,
        "engine_rpm": 1900,
        "engine_load": 55,
        "operating_hours": 2500,
        "mileage": 50000
    },

    # MAINTENANCE REQUIRED
    {
        "vehicle_id": "TRK003",
        "ambient_temp": 32,
        "engine_temp": 105,
        "engine_rpm": 2200,
        "engine_load": 75,
        "operating_hours": 4500,
        "mileage": 90000
    },

    # CRITICAL
    {
        "vehicle_id": "TRK004",
        "ambient_temp": 36,
        "engine_temp": 118,
        "engine_rpm": 2450,
        "engine_load": 95,
        "operating_hours": 8000,
        "mileage": 170000
    },

    # VERY CRITICAL
    {
        "vehicle_id": "TRK005",
        "ambient_temp": 25,
        "engine_temp": 75,
        "engine_rpm": 1500,
        "engine_load": 30,
        "operating_hours": 500,
        "mileage": 10000
    }
]

def generate_telemetry(vehicle_id):

    state = vehicle_state[vehicle_id]

    # small controlled drift (IMPORTANT FIX)
    state["engine_temp"] += random.randint(-2, 3)
    state["engine_rpm"] += random.randint(-50, 50)
    state["engine_load"] += random.randint(-3, 3)
    state["operating_hours"] += 1
    state["mileage"] += random.randint(5, 20)

    # clamp values (prevents chaos)
    state["engine_temp"] = max(60, min(120, state["engine_temp"]))
    state["engine_rpm"] = max(800, min(2500, state["engine_rpm"]))
    state["engine_load"] = max(10, min(100, state["engine_load"]))

    return {
        "vehicle_id": vehicle_id,
        "ambient_temp": 30,
        "engine_temp": state["engine_temp"],
        "engine_rpm": state["engine_rpm"],
        "engine_load": state["engine_load"],
        "operating_hours": state["operating_hours"],
        "mileage": state["mileage"],
    }

if __name__ == "__main__":

    while True:

        for vehicle in vehicles:

            data = generate_telemetry(vehicle["vehicle_id"])

            save_telemetry(data)

            result = process_vehicle_event(data)

            print("Vehicle:", data["vehicle_id"])
            print("Prediction:", result["prediction"])

            if "maintenance" in result:
                print(
                    "Maintenance:",
                    result["maintenance"]
                )

            print("-" * 50)

        time.sleep(5)