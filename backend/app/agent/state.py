from typing import TypedDict

class FleetState(TypedDict, total=False):

    telemetry: dict

    prediction: dict

    maintenance: dict

    has_delivery: bool

    replacement_vehicle: str

    booking: dict