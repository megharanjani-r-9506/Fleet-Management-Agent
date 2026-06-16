from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "fleet.db"

def get_connection():
    return sqlite3.connect(DB_PATH)