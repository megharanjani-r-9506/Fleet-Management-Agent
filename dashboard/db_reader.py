import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "backend" / "fleet.db"


def get_predictions():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM predictions
    ORDER BY id DESC
    LIMIT 20
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def get_maintenance():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM maintenance_schedule
    ORDER BY id DESC
    LIMIT 20
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df

def get_bookings():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM service_bookings
    ORDER BY id DESC
    LIMIT 20
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def get_deliveries():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM delivery_schedule
    ORDER BY id DESC
    LIMIT 20
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def get_service_slots():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM service_slots
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df