from db_reader import (
    get_predictions,
    get_maintenance,
    get_bookings,
    get_deliveries,
    get_service_slots
)

print(get_predictions().head())
print(get_maintenance().head())
print(get_bookings().head())
print(get_deliveries().head())
print(get_service_slots().head())