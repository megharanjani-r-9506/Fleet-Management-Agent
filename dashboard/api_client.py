import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"


def get_vehicles():
    res = requests.get(f"{BASE_URL}/vehicles")
    data = res.json()
    return pd.DataFrame(data)


def get_predictions():
    res = requests.get(f"{BASE_URL}/predictions")
    return pd.DataFrame(res.json())


def get_maintenance():
    res = requests.get(f"{BASE_URL}/maintenance")
    return pd.DataFrame(res.json())


def get_bookings():
    res = requests.get(f"{BASE_URL}/bookings")
    return pd.DataFrame(res.json())


def get_deliveries():
    res = requests.get(f"{BASE_URL}/deliveries")
    return pd.DataFrame(res.json())


def get_service_slots():
    res = requests.get(f"{BASE_URL}/service-slots")
    return pd.DataFrame(res.json())