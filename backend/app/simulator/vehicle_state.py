# app/simulator/vehicle_state.py

import random

# baseline memory for each vehicle
vehicle_state = {

    # HEALTHY
    "TRK001": {
        "engine_temp": 65,
        "engine_rpm": 1000,
        "engine_load": 15,
        "operating_hours": 200,
        "mileage": 5000,
    },

    # HEALTHY / MONITOR BORDER
    "TRK002": {
        "engine_temp": 75,
        "engine_rpm": 1300,
        "engine_load": 30,
        "operating_hours": 1000,
        "mileage": 20000,
    },

    # MONITOR
    "TRK003": {
        "engine_temp": 85,
        "engine_rpm": 1600,
        "engine_load": 45,
        "operating_hours": 2500,
        "mileage": 50000,
    },

    # MAINTENANCE REQUIRED
    "TRK004": {
        "engine_temp": 100,
        "engine_rpm": 2100,
        "engine_load": 70,
        "operating_hours": 5000,
        "mileage": 100000,
    },

    # CRITICAL
    "TRK005": {
        "engine_temp": 120,
        "engine_rpm": 2500,
        "engine_load": 100,
        "operating_hours": 10000,
        "mileage": 200000,
    },
}