from datetime import datetime, timedelta
from app.services.delivery_service import has_upcoming_delivery


# -----------------------------
# PRIORITY SCORES
# -----------------------------
MAINTENANCE_SCORE = {
    "Critical": 10,
    "Maintenance Required": 7,
    "Monitor": 4,
    "Healthy": 1
}


# -----------------------------
# DELIVERY URGENCY SCORE
# -----------------------------
def calculate_delivery_urgency(delivery_date_str):

    delivery_date = datetime.strptime(delivery_date_str, "%Y-%m-%d")
    today = datetime.now()

    days_left = (delivery_date - today).days

    if days_left <= 1:
        return 10
    elif days_left <= 3:
        return 7
    else:
        return 4