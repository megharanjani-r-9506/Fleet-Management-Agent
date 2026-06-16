from app.agent.workflow import fleet_graph


state = {
    "telemetry": {
        "vehicle_id": "TRK001",
        "ambient_temp": 35,
        "engine_temp": 110,
        "engine_rpm": 2500,
        "engine_load": 80,
        "operating_hours": 5000,
        "mileage": 120000
    }
}
result = fleet_graph.invoke(state)

print(result)