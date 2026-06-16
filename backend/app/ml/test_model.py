from app.ml.predictor import predict_vehicle_health

tests = [
    {
        "ambient_temp": 25,
        "engine_temp": 60,
        "engine_rpm": 1000,
        "engine_load": 10,
        "operating_hours": 100,
        "mileage": 1000
    },
    {
        "ambient_temp": 25,
        "engine_temp": 70,
        "engine_rpm": 1200,
        "engine_load": 20,
        "operating_hours": 500,
        "mileage": 10000
    },
    {
        "ambient_temp": 35,
        "engine_temp": 110,
        "engine_rpm": 2500,
        "engine_load": 80,
        "operating_hours": 5000,
        "mileage": 120000
    }
]

for t in tests:
    print(predict_vehicle_health(**t))