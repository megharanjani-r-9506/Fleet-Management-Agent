from app.ml.predictor import predict_vehicle_health
from app.services.maintenance_scheduler import schedule_maintenance
from app.services.delivery_service import has_scheduled_delivery
from app.services.fleet_service import find_replacement_vehicle
from app.services.booking_service import create_booking

def prediction_node(state):

    telemetry = state["telemetry"]

    prediction = predict_vehicle_health(
        ambient_temp=telemetry["ambient_temp"],
        engine_temp=telemetry["engine_temp"],
        engine_rpm=telemetry["engine_rpm"],
        engine_load=telemetry["engine_load"],
        operating_hours=telemetry["operating_hours"],
        mileage=telemetry["mileage"]
    )

    state["prediction"] = prediction

    return state

def maintenance_node(state):

    telemetry = state["telemetry"]

    prediction = state["prediction"]

    maintenance = schedule_maintenance(
        vehicle_id=telemetry["vehicle_id"],
        risk_level=prediction["risk_level"]
    )

    state["maintenance"] = maintenance

    return state

def route_by_risk(state):

    risk = state["prediction"]["risk_level"]

    if risk == "Healthy":
        return "end"

    if risk == "Monitor":
        return "end"

    return "maintenance"


def delivery_check_node(state):

    vehicle_id = state["telemetry"]["vehicle_id"]

    state["has_delivery"] = has_scheduled_delivery(
        vehicle_id
    )

    return state

def replacement_vehicle_node(state):

    vehicle_id = state["telemetry"]["vehicle_id"]

    replacement = find_replacement_vehicle(
        vehicle_id
    )

    state["replacement_vehicle"] = replacement

    return state

def route_after_delivery_check(state):

    if state["has_delivery"]:
        return "replacement"

    return "end"

def booking_node(state):

    vehicle_id = state["telemetry"]["vehicle_id"]

    booking = create_booking(vehicle_id)

    state["booking"] = booking

    return state

def route_after_delivery_check(state):

    if state["has_delivery"]:
        return "replacement"

    return "booking"