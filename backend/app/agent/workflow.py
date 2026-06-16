from langgraph.graph import StateGraph, END
from app.agent.nodes import (
    prediction_node,
    maintenance_node,
    delivery_check_node,
    replacement_vehicle_node,
    booking_node,
    route_by_risk,
    route_after_delivery_check
)
from app.agent.state import FleetState

builder = StateGraph(FleetState)

builder.add_node(
    "prediction",
    prediction_node
)

builder.add_node(
    "maintenance",
    maintenance_node
)

builder.add_node(
    "delivery_check",
    delivery_check_node
)

builder.add_node(
    "replacement_vehicle",
    replacement_vehicle_node
)
builder.add_node(
    "booking",
    booking_node
)

builder.set_entry_point("prediction")

builder.add_conditional_edges(
    "prediction",
    route_by_risk,
    {
        "maintenance": "maintenance",
        "end": END
    }
)

builder.add_edge(
    "maintenance",
    "delivery_check"
)

builder.add_conditional_edges(
    "delivery_check",
    route_after_delivery_check,
    {
        "replacement": "replacement_vehicle",
        "booking": "booking"
    }
)

builder.add_edge(
    "replacement_vehicle",
    "booking"
)

builder.add_edge(
    "booking",
    END
)
fleet_graph = builder.compile()