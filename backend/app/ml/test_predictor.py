from app.ml.predictor import predict_vehicle_health


result = predict_vehicle_health(
    air_temp=310,
    process_temp=320,
    rpm=3000,
    torque=80,
    tool_wear=250
)

print(result)