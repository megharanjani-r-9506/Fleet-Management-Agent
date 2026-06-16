# app/simulator/vehicle_state.py

import random

# baseline memory for each vehicle
vehicle_state = {
    "TRK001": {
        "engine_temp": 70,
        "engine_rpm": 1200,
        "engine_load": 30,
        "operating_hours": 500,
        "mileage": 10000,
    },
    "TRK002": {
        "engine_temp": 65,
        "engine_rpm": 1100,
        "engine_load": 25,
        "operating_hours": 800,
        "mileage": 20000,
    },
    "TRK003": {
        "engine_temp": 85,
        "engine_rpm": 1500,
        "engine_load": 60,
        "operating_hours": 2000,
        "mileage": 50000,
    },
    "TRK004": {
        "engine_temp": 68,
        "engine_rpm": 1000,
        "engine_load": 20,
        "operating_hours": 300,
        "mileage": 8000,
    },
    "TRK005": {
        "engine_temp": 95,
        "engine_rpm": 1800,
        "engine_load": 75,
        "operating_hours": 4000,
        "mileage": 90000,
    },
}