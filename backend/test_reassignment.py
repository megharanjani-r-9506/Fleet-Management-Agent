from app.services.reassignment_service import reassign_delivery

rows = reassign_delivery(
    "TRK001",
    "TRK002"
)

print(rows)