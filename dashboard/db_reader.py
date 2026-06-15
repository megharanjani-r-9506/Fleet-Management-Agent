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