import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "backend" / "fleet.db"


def get_service_slots():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        """
        SELECT *
        FROM service_slots
        ORDER BY service_date
        """,
        conn
    )

    conn.close()

    return df


def get_bookings():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        """
        SELECT *
        FROM service_bookings
        ORDER BY id DESC
        """,
        conn
    )

    conn.close()

    return df